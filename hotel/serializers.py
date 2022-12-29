from django.db import transaction
from django.db.utils import IntegrityError
from django.utils import timezone
from rest_framework import serializers, exceptions

from hotel.models import Hotel, HotelAddress, HotelRating, HotelRoom, HotelReservation
from reservations.base_models.reservation import ReservedStatus
from reservations.base_models.room import RoomStatus
from reservations.models import Payment, PaymentStatus
from reservations.serializers import LocationSerializer, PriceByCurrencySerializer, PaymentSerializer
from reservations.sub_models.price import Price, Currency
from utlis.reservation import convert_payment_status_to_reserved_status


class HotelAddressSerializer(serializers.ModelSerializer):
    location = LocationSerializer(required=False)

    class Meta:
        model = HotelAddress
        fields = ('id', 'phone', 'country', 'city', 'address', 'location', 'zip_code')
        extra_kwargs = {'phone': {'required': False}}


class HotelRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelRating
        fields = ('id', 'hotel', 'user', 'rate',)


class HotelSerializer(serializers.ModelSerializer):
    address = HotelAddressSerializer(many=False)

    class Meta:
        model = Hotel
        fields = ('id', 'name', 'description', 'residence_status', 'address', 'star', 'room_count', 'avatar')

    @transaction.atomic
    def create(self, validated_data):
        address = validated_data.pop('address', None)

        try:
            address = HotelAddress.objects.create(**address)

        except (ValueError, TypeError) as e:
            raise exceptions.ValidationError("invalid data -> {}".format(e))
        except Exception as e:
            raise exceptions.ValidationError("Internal server error -> {}".format(e))

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
        except Exception as e:
            raise exceptions.ValidationError("Internal server error -> {}".format(e))

        instance.save()

        if address:
            hotel_address = HotelAddress.objects.filter(phone=instance.address.phone).get()
            try:
                for attr, value in address.items():
                    setattr(hotel_address, attr, value)

            except (ValueError, TypeError) as e:
                raise exceptions.ValidationError("invalid data -> {}".format(e))
            except Exception as e:
                raise exceptions.ValidationError("Internal server error -> {}".format(e))

            hotel_address.save()
            instance.address = hotel_address

        return instance


# ---------------------------------------------HotelRoom----------------------------------------------------------------

class HotelRoomSerializer(serializers.ModelSerializer):
    price_per_night = PriceByCurrencySerializer()

    class Meta:
        model = HotelRoom
        fields = ('id', 'number', 'capacity', 'status', 'description', 'price_per_night', 'hotel', 'avatar')

    @transaction.atomic
    def create(self, validated_data):
        price_per_night = validated_data.pop('price_per_night', None)
        currency = price_per_night.pop('currency', None)

        try:
            currency, _ = Currency.objects.get_or_create(name=currency.get('name', None),
                                                         defaults={"code": currency.get('code', None)})
            price = Price.objects.create(currency=currency, **price_per_night)

        except (ValueError, TypeError) as e:
            raise exceptions.ValidationError("invalid data -> {}".format(e))
        except Exception as e:
            raise exceptions.ValidationError("Internal server error -> {}".format(e))

        hotel_room = HotelRoom.objects.create(price_per_night=price, **validated_data)

        return hotel_room

    @transaction.atomic
    def update(self, instance, validated_data):
        price_per_night = validated_data.pop('price_per_night', None)
        currency = price_per_night.pop('currency', None)

        try:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
        except HotelRoom.DoesNotExist:
            raise exceptions.ValidationError("invalid data")

        instance.save()

        if price_per_night:
            if currency:
                currency_room = Currency.objects.filter(id=instance.price_per_night.currency.id).get()
                try:
                    for attr, value in currency.items():
                        setattr(currency_room, attr, value)
                except Currency.DoesNotExist:
                    raise exceptions.ValidationError("invalid data")
                currency_room.save()

            price = Price.objects.filter(id=instance.price_per_night.id).get()
            try:
                for attr, value in price_per_night.items():
                    setattr(price, attr, value)
            except Price.DoesNotExist:
                raise exceptions.ValidationError("invalid data")
            price.save()
            instance.price_per_night = price

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

    def get_total_cost(self, obj):
        return {"cost": (obj.adult_count + obj.children_count * 0.5) * obj.room.price_per_night.value,
                "currency": obj.room.price_per_night.currency.code}

    @transaction.atomic
    def create(self, validated_data):
        try:
            reserve = HotelReservation.objects.create(**validated_data)
            Payment.objects.create(user=reserve.user, reserved_key=reserve.reserved_key)
        except (ValueError, TypeError) as e:
            raise exceptions.ValidationError("invalid data -> {}".format(e))
        except IntegrityError:
            raise exceptions.ValidationError("Each user has only one record reserved room!")
        except Exception as e:
            raise exceptions.ValidationError("Internal server error -> {}".format(e))
        return reserve


# ---------------------------------------------ResultReservation-------------------------------------------------------

@transaction.atomic
def update_reservation(request, *args, **kwargs):
    reserved_key = kwargs['reserved_key']
    if 'payment_status' in request.data:
        status = request.data['payment_status']
        try:
            payment_status = PaymentStatus(status)
        except (ValueError, TypeError) as e:
            raise exceptions.ValidationError("invalid data -> {}".format(e))
    else:
        raise exceptions.ValidationError("payment_status required")

        # reserve -> change ,payment -> change, room -> change
    try:
        reserve = HotelReservation.objects.filter(reserved_key=reserved_key).get()
        if reserve.reserved_status == ReservedStatus.INITIAL:
            reserved_status = convert_payment_status_to_reserved_status(payment_status)
            reserve.reserved_status = reserved_status
            reserve.save()
        else:
            raise exceptions.ValidationError("This reserved: {} not initial".format(reserved_key))

        payment = Payment.objects.filter(reserved_key=reserved_key).get()
        if payment.payment_status in [PaymentStatus.INITIAL, PaymentStatus.FAILED]:
            payment.payment_status = payment_status
            payment.save()
        else:
            raise exceptions.ValidationError("Payment for this reserved: {} invalid".format(reserved_key))

        room = reserve.room
        if reserved_status == ReservedStatus.RESERVED:
            if room.status == RoomStatus.FREE:
                room.status = RoomStatus.RESERVED
                room.save()
            else:
                raise exceptions.ValidationError("Room for this reserved: {} invalid".format(reserved_key))

    except Payment.DoesNotExist:
        raise exceptions.ValidationError("Payment with this reserved_key :{} not existed".format(reserved_key))
    except HotelReservation.DoesNotExist:
        raise exceptions.ValidationError("Reservation with this reserved_key :{} not existed".format(reserved_key))
    except HotelRoom.DoesNotExist:
        raise exceptions.ValidationError("Room with this reserved not existed")
    except IntegrityError as e:
        raise exceptions.ValidationError("Error: {}".format(e))
    except (ValueError, TypeError) as e:
        raise exceptions.ValidationError("invalid data -> {}".format(e))
    except Exception as e:
        raise exceptions.ValidationError("Internal server error -> {}".format(e))

    return {"room": HotelRoomSerializer(room).data, "reserve": HotelReservationSerializer(reserve).data}
