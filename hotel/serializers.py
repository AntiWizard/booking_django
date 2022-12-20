from rest_framework import serializers

from hotel.models import Hotel, HotelAddress, HotelRating
from reservations.sub_models.location import Location
from reservations.sub_models.type import PlaceType
from reservations.sub_serializers import LocationSerializer, PlaceTypeSerializer


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
    rate = HotelRateSerializer(required=False)
    type = PlaceTypeSerializer()

    class Meta:
        model = Hotel
        fields = ('name', 'description', 'type', 'address', 'star', 'room_count', 'avatar')

    def create(self, validated_data):
        address = validated_data.pop('address') if 'address' in validated_data else None
        type = validated_data.pop('type') if 'type' in validated_data else None
        location = address.pop('location') if address and 'location' in address else None

        location, _ = Location.objects.get_or_create(x_coordination=location['x_coordination'],
                                                     y_coordination=location['y_coordination'],
                                                     defaults={"x_coordination": location['x_coordination'],
                                                               "y_coordination": location['y_coordination']})

        address = HotelAddress.objects.create(location=location, **address)
        type, _ = PlaceType.objects.get_or_create(title=type['title'], defaults={"title": type['title']})

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
