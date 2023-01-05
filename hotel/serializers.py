from django.db import transaction
from django.db.utils import IntegrityError
from django.utils import timezone
from rest_framework import serializers, exceptions

from hotel.models import *
from reservations.base_models.comment import CommentStatus
from reservations.base_models.passenger import PassengerType
from reservations.base_models.reservation import ReservedStatus
from reservations.base_models.residence import ResidenceStatus
from reservations.base_models.room import RoomStatus
from reservations.models import Payment, PaymentStatus
from reservations.serializers import LocationSerializer, PriceByCurrencySerializer, PaymentSerializer
from reservations.sub_models.price import Price, Currency
from utlis.calc_age import calc_age
from utlis.check_obj import check_status_in_request_data, check_reserved_key_existed
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


# ---------------------------------------------HotelPassenger--------------------------------------------------------

class HotelPassengerSerializer(serializers.ModelSerializer):
    room = HotelRoomSerializer(required=False)

    class Meta:
        model = HotelPassenger
        fields = (
            'id', 'passenger_code', 'parent', 'room', 'phone', 'national_id', 'birth_day', 'first_name', 'last_name',
            'stay_status', 'passenger_type',)

        extra_kwargs = {"parent": {'required': False}}


# ---------------------------------------------HotelReservation---------------------------------------------------------

class HotelReservationSerializer(serializers.ModelSerializer):
    total_cost = serializers.SerializerMethodField()
    payment = PaymentSerializer(many=False, required=False)
    passenger = HotelPassengerSerializer(many=True, required=False)

    class Meta:
        model = HotelReservation
        fields = (
            'id', 'user', 'reserved_status', 'passenger_count', 'total_cost', 'room', 'check_in_date',
            'check_out_date', 'payment', 'passenger',)

    def get_total_cost(self, obj):
        return {"cost": obj.passenger_count * obj.room.hotel.price_per_night.value,
                "currency": obj.room.hotel.price_per_night.currency.code}

    def validate(self, data):

        if not (data['check_out_date'] > data['check_in_date'] >= timezone.now().date()):
            raise exceptions.ValidationError({"check_out_date with check_in_date": "invalid date"})

        if self.context['request'].method == "POST" and data["room"].status != RoomStatus.FREE:
            raise exceptions.ValidationError(
                {"Room {} cant creatable!".format(RoomStatus(data['room'].status))})

        if self.context['request'].method in ["PUT", "PATCH", "DELETE"] \
                and data["room"].status not in [RoomStatus.INITIAL, RoomStatus.RESERVED]:
            raise exceptions.ValidationError(
                {"Room {} cant updatable!".format(RoomStatus(data['room'].status))})

        if data["room"].capacity < data["passenger_count"]:
            raise exceptions.ValidationError("Need to get more room for this count of passengers")

        return data

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        payment = Payment.objects.filter(reserved_key=instance.reserved_key).get()
        ret['payment'] = PaymentSerializer(payment).data

        passengers = HotelPassenger.objects.filter(reserved_key=instance.reserved_key).all()
        ret['passengers'] = HotelPassengerSerializer(passengers, many=True).data

        return ret

    @transaction.atomic
    def create(self, validated_data):
        room = validated_data['room']
        passengers = validated_data.pop('passenger', None)

        if len(passengers) != validated_data['passenger_count']:
            raise exceptions.ValidationError("passenger information uncompleted!")

        try:
            reserve = HotelReservation.objects.create(**validated_data)
            Payment.objects.create(user=reserve.user, reserved_key=reserve.reserved_key)

            create_passengers = []

            for passenger in passengers:
                _passenger = HotelPassenger(room=room, reserved_key=reserve.reserved_key,
                                            parent=validated_data['user'], **passenger)
                if calc_age(passenger['birth_day']) < 18:
                    _passenger.passenger_type = PassengerType.CHILDREN

                create_passengers.append(_passenger)

            HotelPassenger.objects.bulk_create(create_passengers)

            room.status = RoomStatus.INITIAL
            room.save()

            check_and_update_if_hotel_full(room.hotel_id)

        except (ValueError, TypeError) as e:
            raise exceptions.ValidationError("invalid data -> {}".format(e))
        except IntegrityError:
            raise exceptions.ValidationError("Each user has only one record reserved room!")
        except HotelRoom.DoesNotExist:
            raise exceptions.ValidationError("This room not reservable")
        except Exception as e:
            raise exceptions.ValidationError("Error: {}".format(e))

        return reserve

    @transaction.atomic
    def update(self, instance, validated_data):
        reserved_key = instance.reserved_key

        passengers = validated_data.pop('passenger', None)

        if instance.passenger_count != validated_data['passenger_count']:
            raise exceptions.ValidationError("passenger information uncompleted!")

        old_passengers = HotelPassenger.objects.filter(
            reserved_key=reserved_key, stay_status=StayStatus.INITIAL).all()

        try:
            for passenger in passengers:
                update_passenger = old_passengers.filter(national_id=passenger['national_id'])
                if update_passenger.exists():
                    update_passenger.update(**passenger)
                else:
                    raise exceptions.ValidationError("Passenger info not existed")

        except (ValueError, TypeError) as e:
            raise exceptions.ValidationError("invalid data -> {}".format(e))
        except IntegrityError as e:
            raise exceptions.ValidationError("Each user has only one record reserved seat!")
        except Exception as e:
            raise e

        return instance


@transaction.atomic
def cancel_hotel_reservation(instance):
    room = instance.room

    try:
        payment = Payment.objects.filter(reserved_key=instance.reserved_key, payment_status=PaymentStatus.SUCCESS).get()
        passengers = HotelPassenger.objects.filter(reserved_key=instance.reserved_key,
                                                   stay_status=StayStatus.RESERVED).all()

        if instance.reserved_status == ReservedStatus.RESERVED and payment \
                and passengers.count() == instance.passenger_count:

            payment.payment_status = PaymentStatus.CANCELLED
            payment.save()

            instance.reserved_status = ReservedStatus.CANCELLED
            instance.save()

            update_passengers = []
            for passenger in passengers:
                if passenger.stay_status == StayStatus.RESERVED:
                    passenger.stay_status = StayStatus.CANCELLED
                    update_passengers.append(passenger)

                else:
                    raise exceptions.ValidationError("This passenger :{} transfer_status invalid".format(passenger.id))

            HotelPassenger.objects.bulk_update(update_passengers, fields=['stay_status'])

            if room.status == RoomStatus.RESERVED:
                room.status = RoomStatus.FREE
                room.save()
            else:
                raise exceptions.ValidationError("This room :{} room status invalid".format(room.number))

            if room.hotel.residence_status == ResidenceStatus.FULL:
                room.hotel.residence_status = ResidenceStatus.SPACE
                room.hotel.save()

        else:
            raise exceptions.ValidationError(
                "This instance :{} reserved_status invalid".format(instance.reserved_status))

    except (ValueError, TypeError) as e:
        raise exceptions.ValidationError("invalid data -> {}".format(e))
    except Exception as e:
        raise exceptions.ValidationError("Error: {}".format(e))


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

        passengers = check_reserved_key_existed(reserved_key, HotelPassenger, True)
        room = reserve.room
        if reserved_status == ReservedStatus.RESERVED:
            passengers_update = []
            for passenger in passengers:
                if passenger.stay_status == StayStatus.INITIAL:
                    passenger.stay_status = StayStatus.RESERVED
                    passengers_update.append(passenger)

                else:
                    raise exceptions.ValidationError(
                        "Passenger info for this reserved: {} was invalid".format(reserved_key))

            if room.status == RoomStatus.INITIAL:
                room.status = RoomStatus.RESERVED
                room.save()
                HotelPassenger.objects.bulk_update(passengers_update, fields=['stay_status'])
                check_and_update_if_hotel_full(room.hotel_id)
            else:
                raise exceptions.ValidationError("Room for this reserved: {} was invalid".format(reserved_key))


    except IntegrityError as e:
        raise exceptions.ValidationError("Error: {}".format(e))
    except (ValueError, TypeError) as e:
        raise exceptions.ValidationError("invalid data -> {}".format(e))
    except Exception as e:
        raise exceptions.ValidationError("Error: {}".format(e))

    return {"reserve": HotelReservationSerializer(reserve).data}


def check_and_update_if_hotel_full(hotel_id):
    free_room = HotelRoom.objects.filter(hotel__id=hotel_id, status=RoomStatus.FREE, is_valid=True)
    if not free_room.exists():
        return Hotel.objects.filter(id=hotel_id, is_valid=True).update(residence_status=ResidenceStatus.FULL)
    return


# ---------------------------------------------UpdateHotelComment-------------------------------------------------------

@transaction.atomic
def update_hotel_comment(request, **kwargs):
    comment_id = kwargs['pk']

    status = check_status_in_request_data('status', request.data, CommentStatus)

    if status not in [CommentStatus.APPROVED, CommentStatus.REJECTED]:
        raise exceptions.ValidationError("invalid status :{}".format(status))

    try:
        comment = HotelComment.objects.filter(id=comment_id).get()
        if comment.status != CommentStatus.CREATED:
            raise exceptions.ValidationError("This comment checked")
        comment.status = status
        comment.validated_by = request.user
        comment.save()

    except HotelComment.DoesNotExist:
        raise exceptions.ValidationError("This comment does not exist")

    return HotelCommentForUpdatedSerializer(comment).data
