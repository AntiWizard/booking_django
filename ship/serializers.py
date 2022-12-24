from django.db import transaction
from rest_framework import serializers

from reservations.serializers import LocationSerializer
from ship.models import Ship, ShipAddress, ShipRating


class ShipAddressSerializer(serializers.ModelSerializer):
    location = LocationSerializer(required=False)

    class Meta:
        model = ShipAddress
        fields = ('phone', 'country', 'city', 'address', 'location',)


class ShipRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShipRating
        fields = ('Ship', 'user', 'rate',)


class ShipSerializer(serializers.ModelSerializer):
    source = ShipAddressSerializer()
    destination = ShipAddressSerializer()

    class Meta:
        model = Ship
        fields = ('captain', 'description', 'transport_status', 'max_reservation', 'number_reserved', 'source',
                  'destination',)

    @transaction.atomic
    def create(self, validated_data):
        source = validated_data.pop('source') if 'source' in validated_data else None
        destination = validated_data.pop('destination') if 'destination' in validated_data else None
        type = validated_data.pop('type') if 'type' in validated_data else None

        source = ShipAddress.objects.create(**source)
        destination = ShipAddress.objects.create(**destination)

        ship = Ship.objects.create(source=source, destination=destination, type=type, **validated_data)

        return ship
