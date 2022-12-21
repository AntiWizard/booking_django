from django.db import transaction
from rest_framework import serializers

from airplane.models import Airplane, AirplaneAddress, AirplaneRating
from reservations.sub_models.type import TransportType
from reservations.sub_serializers import LocationSerializer, TransportTypeSerializer


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
    address = AirplaneAddressSerializer()
    rate = AirplaneRateSerializer(required=False)
    type = TransportTypeSerializer()

    class Meta:
        model = Airplane
        fields = ('pilot', 'description', 'type', 'status', 'max_reservation', 'number_reserved', 'source',
                  'destination',)

    @transaction.atomic
    def create(self, validated_data):
        source = validated_data.pop('source') if 'source' in validated_data else None
        destination = validated_data.pop('destination') if 'destination' in validated_data else None
        type = validated_data.pop('type') if 'type' in validated_data else None

        source = AirplaneAddress.objects.create(**source)
        destination = AirplaneAddress.objects.create(**destination)

        type, _ = TransportType.objects.get_or_create(title=type['title'], defaults={"title": type['title']})

        airplane = Airplane.objects.create(source=source, destination=destination, type=type, **validated_data)
        return airplane
