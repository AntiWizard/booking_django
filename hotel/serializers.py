from django.db import transaction
from django.db.utils import IntegrityError
from django.utils import timezone
from rest_framework import serializers, exceptions

from hotel.models import *
from reservations.base_models.comment import CommentStatus
from reservations.base_models.reservation import ReservedStatus
from reservations.base_models.residence import ResidenceStatus
from reservations.base_models.room import RoomStatus
from reservations.models import Payment, PaymentStatus
from reservations.serializers import LocationSerializer, PriceByCurrencySerializer, PaymentSerializer
from reservations.sub_models.price import Price, Currency
from utlis.check_obj_hotel import check_status_in_request_data, check_reserved_key_existed
from utlis.reservation import convert_payment_status_to_reserved_status


# ---------------------------------------------HotelAddress-------------------------------------------------------------


class HotelAddressSerializer(serializers.ModelSerializer):
    location = LocationSerializer(required=False)

    class Meta:
        model = HotelAddress
        fields = ('id', 'phone', 'country', 'city', 'address', 'location', 'zip_code')
        extra_kwargs = {'phone': {'required': False}}


# ---------------------------------------------HotelRate----------------------------------------------------------------

class HotelRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelRating
        fields = ('id', 'hotel', 'user', 'rate',)


# ---------------------------------------------HotelComment----------------------------------------------------------------
class HotelCommentForCreatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelComment
        fields = ('id', 'hotel', 'user', 'status', 'parent', 'comment_body', 'validated_by')
        extra_kwargs = {"parent": {"required": False}}


class HotelCommentForUpdatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelComment
        fields = ('id', 'status', 'comment_body', 'validated_by')
        extra_kwargs = {"validated_by": {"required": False, "read_only": True}}

    def update(self, instance, validated_data):
        if instance.status not in [CommentStatus.CREATED]:
            raise exceptions.ValidationError("Comment with result cant be update")

        if instance.comment_body == validated_data['comment_body']:
            return instance

        try:
            instance.comment_body = validated_data['comment_body']
            instance.validated_by = None

        except (ValueError, TypeError) as e:
            raise exceptions.ValidationError("invalid data -> {}".format(e))

        instance.save()

        return instance


# ----------------------------------------------HotelGallery------------------------------------------------------------
class HotelGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelGallery
        fields = ('id', 'hotel', 'name',)


class HotelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelImage
        fields = ('id', 'gallery', 'is_main', 'image',)


# ---------------------------------------------Hotel--------------------------------------------------------------------

class HotelSerializer(serializers.ModelSerializer):
    address = HotelAddressSerializer(many=False)
    price_per_night = PriceByCurrencySerializer(many=False, required=False, read_only=True)

    class Meta:
        model = Hotel
        fields = ('id', 'name', 'description', 'average_rating', 'residence_status', 'address',
                  "price_per_night", 'star', 'room_count',)
        extra_kwargs = {"average_rating": {"required": False, "read_only": True}}

    @transaction.atomic
    def create(self, validated_data):
        address = validated_data.pop('address', None)

        try:
            address = HotelAddress.objects.create(**address)

        except (ValueError, TypeError) as e:
            raise exceptions.ValidationError("invalid data -> {}".format(e))

        hotel = Hotel.objects.create(address=address, **validated_data)

        return hotel

    @transaction.atomic
    def update(self, instance, validated_data):
        address = validated_data.pop('address', None)

        try:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)

        except (ValueError, TypeError) as e:
            raise exceptions.ValidationError("invalid data -> {}".format(e))

        instance.save()

        if address:
            hotel_address = HotelAddress.objects.filter(phone=instance.address.phone).get()
            try:
                for attr, value in address.items():
                    setattr(hotel_address, attr, value)

            except (ValueError, TypeError) as e:
                raise exceptions.ValidationError("invalid data -> {}".format(e))

            hotel_address.save()
            instance.address = hotel_address

        return instance


# ---------------------------------------------HotelRoom----------------------------------------------------------------

class HotelRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelRoom
        fields = ('id', 'number', 'capacity', 'status', 'description', 'price', 'hotel', 'avatar')

    @transaction.atomic
    def create(self, validated_data):
        price = validated_data.pop('price', None)
        currency = price.pop('currency', None)
        try:
            currency, _ = Currency.objects.get_or_create(name=currency.get('name', None),
                                                         defaults={"code": currency.get('code', None)})
            price = Price.objects.create(currency=currency, **price)

        except (ValueError, TypeError) as e:
            raise exceptions.ValidationError("invalid data -> {}".format(e))

        hotel_room = HotelRoom.objects.create(price=price, **validated_data)
        super(HotelRoomSerializer, self).create()
        return hotel_room

    @transaction.atomic
    def update(self, instance, validated_data):
        price = validated_data.pop('price', None)
        currency = price.pop('currency', None)

        try:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
        except HotelRoom.DoesNotExist:
            raise exceptions.ValidationError("invalid data")

        instance.save()

        if price:
            if currency:
                currency_room = Currency.objects.filter(id=instance.price.currency.id).get()
                try:
                    for attr, value in currency.items():
                        setattr(currency_room, attr, value)
                except Currency.DoesNotExist:
                    raise exceptions.ValidationError("invalid data")
                currency_room.save()

            _price = Price.objects.filter(id=instance.price.id).get()
            try:
                for attr, value in price.items():
                    setattr(_price, attr, value)
            except Price.DoesNotExist:
                raise exceptions.ValidationError("invalid data")
            _price.save()
            instance.price = price

        return instance


# ---------------------------------------------HotelReservation---------------------------------------------------------

class HotelReservationSerializer(serializers.ModelSerializer):
    total_cost = serializers.SerializerMethodField()
    payment = PaymentSerializer(many=False, required=False)

    class Meta:
        model = HotelReservation
        fields = (
            'id', 'user', 'reserved_status', 'adult_count', 'children_count', 'total_cost', 'room', 'check_in_date',
            'check_out_date', 'payment',)

    def get_total_cost(self, obj):
        return {"cost": (obj.adult_count + obj.children_count * 0.5) * obj.room.price.value,
                "currency": obj.room.price.currency.code}

    def validate(self, data):
        if not (data['check_out_date'] > data['check_in_date'] >= timezone.now().date()):
            raise exceptions.ValidationError({"check_out_date with check_in_date": "invalid date"})

        if data["room"].status != RoomStatus.FREE:
            raise exceptions.ValidationError(
                {"room number": "Room {} for this room number!".format(RoomStatus(data['room'].status))})

        if data["room"].capacity < data["adult_count"] + data["children_count"]:
            raise exceptions.ValidationError({
                "adult_count with children_count": "Room has {} capacity for this room number!".format(
                    data["room"].capacity)})

        return data

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        payment = Payment.objects.filter(reserved_key=instance.reserved_key).get()
        ret['payment'] = PaymentSerializer(payment).data

        ret['room'] = instance.room.number

        return ret

    @transaction.atomic
    def create(self, validated_data):
        try:
            reserve = HotelReservation.objects.create(**validated_data)
            Payment.objects.create(user=reserve.user, reserved_key=reserve.reserved_key)
        except (ValueError, TypeError) as e:
            raise exceptions.ValidationError("invalid data -> {}".format(e))
        except IntegrityError:
            raise exceptions.ValidationError("Each user has only one record reserved room!")
        return reserve


# ---------------------------------------------ResultReservation-------------------------------------------------------

@transaction.atomic
def update_reservation(request, **kwargs):
    reserved_key = kwargs['reserved_key']
    payment_status = check_status_in_request_data('payment_status', request.data, PaymentStatus)

    # reserve -> change ,payment -> change, room -> change
    try:
        reserve = check_reserved_key_existed(reserved_key, HotelReservation)
        if reserve.reserved_status == ReservedStatus.INITIAL:
            reserved_status = convert_payment_status_to_reserved_status(payment_status)
            reserve.reserved_status = reserved_status
            reserve.save()
        else:
            raise exceptions.ValidationError("This reserved: {} not initial".format(reserved_key))

        payment = check_reserved_key_existed(reserved_key, Payment)
        if payment.payment_status in [PaymentStatus.INITIAL, PaymentStatus.FAILED]:
            payment.payment_status = payment_status
            payment.save()
        else:
            raise exceptions.ValidationError("Payment for this reserved: {} was invalid".format(reserved_key))

        room = reserve.room
        if reserved_status == ReservedStatus.RESERVED:
            if room.status == RoomStatus.FREE:
                room.status = RoomStatus.RESERVED
                room.save()
                check_and_update_if_hotel_full(room.hotel.id)
            else:
                raise exceptions.ValidationError("Room for this reserved: {} was invalid".format(reserved_key))

    except IntegrityError as e:
        raise exceptions.ValidationError("Error: {}".format(e))
    except (ValueError, TypeError) as e:
        raise exceptions.ValidationError("invalid data -> {}".format(e))

    return {"reserve": HotelReservationSerializer(reserve).data}


def check_and_update_if_hotel_full(hotel_id):
    free_room = HotelRoom.objects.filter(hotel__id=hotel_id, status=RoomStatus.FREE)
    if not free_room.exists():
        return Hotel.objects.filter(id=hotel_id).update(residence_status=ResidenceStatus.FULL)
    return


@transaction.atomic
def update_hotel_comment(request, **kwargs):
    comment_id = kwargs['pk']

    status = check_status_in_request_data('status', request.data, CommentStatus)

    if status not in [CommentStatus.APPROVED, CommentStatus.REJECTED]:
        raise exceptions.ValidationError("invalid status :{}".format(status))

    try:
        comment = HotelComment.objects.filter(id=comment_id, status=CommentStatus.CREATED).get()
        comment.status = status
        comment.validated_by = request.user
        comment.save()

    except HotelComment.DoesNotExist:
        raise exceptions.ValidationError("status required")

    return HotelCommentForUpdatedSerializer(comment).data
