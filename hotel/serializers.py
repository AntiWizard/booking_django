from django.db import transaction
from rest_framework import serializers

from hotel.models import Hotel, HotelAddress, HotelRating
from reservations.serializers import LocationSerializer, ResidenceTypeSerializer
from reservations.sub_models.type import ResidenceType


class HotelAddressSerializer(serializers.ModelSerializer):
    location = LocationSerializer(required=False)

    class Meta:
        model = HotelAddress
        fields = ('phone', 'country', 'city', 'address', 'location', 'zip_code')


class HotelRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelRating
        fields = ('hotel', 'user', 'rate',)


class HotelSerializer(serializers.ModelSerializer):
    address = HotelAddressSerializer()
    type = ResidenceTypeSerializer()

    class Meta:
        model = Hotel
        fields = ('name', 'description', 'type', 'address', 'star', 'room_count', 'avatar')

    @transaction.atomic
    def create(self, validated_data):
        address = validated_data.pop('address') if 'address' in validated_data else None
        type = validated_data.pop('type') if 'type' in validated_data else None

        address = HotelAddress.objects.create(**address)
        type, _ = ResidenceType.objects.get_or_create(title=type['title'], defaults={"title": type['title']})

        hotel = Hotel.objects.create(address=address, type=type, **validated_data)

        return hotel

        # def update(self, instance, validated_data):
        #     address = validated_data.pop('address')
        #     rate = validated_data.pop('rate')
        #     user_rate = validated_data.pop('user')
        #     type = validated_data.pop('type')
        #
        #     hotel = Hotel.objects.create(**validated_data)
        #
        #     rate = PlaceRate.objects.create(hotel=hotel, user_id=user_rate['id'], rate=rate['rate'])
        #     type = PlaceType.objects.create(hotel=hotel, type=type['title'])
        #
        #     return instance
