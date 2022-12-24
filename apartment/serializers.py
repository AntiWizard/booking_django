from django.db import transaction
from rest_framework import serializers

from apartment.models import ApartmentRating, ApartmentAddress, Apartment
from reservations.serializers import LocationSerializer


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

    class Meta:
        model = Apartment
        fields = ('name', 'description', 'residence_status', 'address', 'unit_count', 'avatar')

    @transaction.atomic
    def create(self, validated_data):
        address = validated_data.pop('address') if 'address' in validated_data else None
        type = validated_data.pop('type') if 'type' in validated_data else None

        address = ApartmentAddress.objects.create(**address)

        apartment = Apartment.objects.create(address=address, type=type, **validated_data)

        return apartment
