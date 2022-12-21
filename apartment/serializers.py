from django.db import transaction
from rest_framework import serializers

from apartment.models import ApartmentRating, ApartmentAddress, Apartment
from reservations.sub_models.location import Location
from reservations.sub_models.type import ResidenceType
from reservations.sub_serializers import ResidenceTypeSerializer, LocationSerializer


class ApartmentAddressSerializer(serializers.ModelSerializer):
    location = LocationSerializer(required=False)

    class Meta:
        model = ApartmentAddress
        fields = ('phone', 'country', 'city', 'address', 'location', 'zip_code')


class ApartmentRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApartmentRating
        fields = ('apartment', 'user', 'rate',)


class ApartmentSerializer(serializers.ModelSerializer):
    address = ApartmentAddressSerializer()
    rate = ApartmentRateSerializer(required=False)
    type = ResidenceTypeSerializer()

    class Meta:
        model = Apartment
        fields = ('name', 'description', 'type', 'address', 'unit_count', 'avatar')

    @transaction.atomic
    def create(self, validated_data):
        address = validated_data.pop('address') if 'address' in validated_data else None
        type = validated_data.pop('type') if 'type' in validated_data else None
        location = address.pop('location') if address and 'location' in address else None

        location, _ = Location.objects.get_or_create(x_coordination=location['x_coordination'],
                                                     y_coordination=location['y_coordination'],
                                                     defaults={"x_coordination": location['x_coordination'],
                                                               "y_coordination": location['y_coordination']})

        address = ApartmentAddress.objects.create(location=location, **address)
        type, _ = ResidenceType.objects.get_or_create(title=type['title'], defaults={"title": type['title']})

        apartment = Apartment.objects.create(address=address, type=type, **validated_data)

        return apartment
