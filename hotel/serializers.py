from django.db import transaction
from rest_framework import serializers, exceptions

from hotel.models import Hotel, HotelAddress, HotelRating, HotelRoom, HotelReservation
from reservations.serializers import LocationSerializer, PriceByCurrencySerializer
from reservations.sub_models.price import Price, Currency


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
        except Exception:
            raise exceptions.ValidationError("invalid address")

        hotel = Hotel.objects.create(address=address, **validated_data)

        return hotel

    @transaction.atomic
    def update(self, instance, validated_data):
        address = validated_data.pop('address', None)

        try:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
        except Exception:
            raise exceptions.ValidationError("invalid data")

        instance.save()

        if address:
            hotel_address = HotelAddress.objects.filter(phone=instance.address.phone).get()
            try:
                for attr, value in address.items():
                    setattr(hotel_address, attr, value)
            except Exception:
                raise exceptions.ValidationError("invalid data")
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
        except Exception:
            raise exceptions.ValidationError("invalid data")

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

    class Meta:
        model = HotelReservation
        fields = (
            'id', 'user', 'reserved_status', 'adult_count', 'children_count', 'total_cost', 'room', 'check_in_date',
            'check_out_date',)

    def get_total_cost(self, obj):
        return {"cost": (obj.adult_count + obj.children_count) * obj.room.price_per_night.value,
                "currency": obj.room.price_per_night.currency.code}

    @transaction.atomic
    def create(self, validated_data):
        reserve = HotelReservation.objects.create(**validated_data)
        return reserve


class SuccessReservationSerializer(serializers.ModelSerializer):
    total_cost = serializers.SerializerMethodField()
    room = serializers.SerializerMethodField()

    class Meta:
        model = HotelReservation
        fields = (
            'id', 'user', 'reserved_status', 'adult_count', 'children_count', 'total_cost', 'room', 'check_in_date',
            'check_out_date',)
        extra_kwargs = {'user': {"required": False, "read_only": True},
                        "total_cost": {"required": False, "read_only": True}}

    def get_room(self, obj):
        return obj.room.status

    def get_total_cost(self, obj):
        return {"cost": (obj.adult_count + obj.children_count) * obj.room.price_per_night.value,
                "currency": obj.room.price_per_night.currency.code}
