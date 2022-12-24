from django.db import transaction
from rest_framework import serializers

from airplane.models import Airplane, AirplaneAddress, AirplaneRating
from reservations.serializers import LocationSerializer


class AirplaneAddressSerializer(serializers.ModelSerializer):
    location = LocationSerializer(required=False)

    class Meta:
        model = AirplaneAddress
        fields = ('phone', 'country', 'city', 'address', 'location',)


class AirplaneRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneRating
        fields = ('airplane', 'user', 'rate',)


class AirplaneSerializer(serializers.ModelSerializer):
    source = AirplaneAddressSerializer()
    destination = AirplaneAddressSerializer()

    class Meta:
        model = Airplane
        fields = ('pilot', 'description', 'transport_status', 'max_reservation', 'number_reserved', 'source',
                  'destination',)

    @transaction.atomic
    def create(self, validated_data):
        source = validated_data.pop('source') if 'source' in validated_data else None
        destination = validated_data.pop('destination') if 'destination' in validated_data else None
        type = validated_data.pop('type') if 'type' in validated_data else None

        source = AirplaneAddress.objects.create(**source)
        destination = AirplaneAddress.objects.create(**destination)

        airplane = Airplane.objects.create(source=source, destination=destination, type=type, **validated_data)
        return airplane
