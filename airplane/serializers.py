from rest_framework import serializers

from hotel.models import Hotel, HotelAddress, HotelRating
from reservations.sub_models.location import Location
from reservations.sub_models.type import PlaceType
from reservations.sub_serializers import LocationSerializer, PlaceTypeSerializer


class ApartmentAddressSerializer(serializers.ModelSerializer):
    location = LocationSerializer(required=False)

    class Meta:
        model = HotelAddress
        fields = ('phone', 'country', 'city', 'address', 'location', 'zip_code')


class ApartmentRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelRating
        fields = ('hotel', 'user', 'rate',)


class ApartmentSerializer(serializers.ModelSerializer):
    address = ApartmentAddressSerializer()
    rate = ApartmentRateSerializer(required=False)
    type = PlaceTypeSerializer()

    class Meta:
        model = Hotel
        fields = ('name', 'description', 'type', 'rate', 'address', 'star', 'max_reservation', 'avatar')

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

        hotel = Hotel.objects.create(address=address, rate=HotelRating.objects.get(id=1), type=type, **validated_data)

        return hotel
