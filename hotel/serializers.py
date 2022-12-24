from django.db import transaction
from rest_framework import serializers, exceptions

from hotel.models import Hotel, HotelAddress, HotelRating
from reservations.serializers import LocationSerializer


class HotelAddressSerializer(serializers.ModelSerializer):
    location = LocationSerializer(required=False)

    class Meta:
        model = HotelAddress
        fields = ('id', 'phone', 'country', 'city', 'address', 'location', 'zip_code')


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

        hotel = Hotel.objects.create(address=address, type=type, **validated_data)

        return hotel

    @transaction.atomic
    def update(self, instance, validated_data):
        address = validated_data.pop('address')
        rate = validated_data.pop('rate')
        user_rate = validated_data.pop('user')
        type = validated_data.pop('type')

        hotel = Hotel.objects.create(**validated_data)

        # rate = PlaceRate.objects.create(hotel=hotel, user_id=user_rate['id'], rate=rate['rate'])
        # type = PlaceType.objects.create(hotel=hotel, type=type['title'])

        return instance
