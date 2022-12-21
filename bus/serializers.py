from rest_framework import serializers

from bus.models import Bus, BusAddress, BusRating
from reservations.sub_models.type import TransportType
from reservations.sub_serializers import LocationSerializer, TransportTypeSerializer


class BusAddressSerializer(serializers.ModelSerializer):
    location = LocationSerializer(required=False)

    class Meta:
        model = BusAddress
        fields = ('phone', 'country', 'city', 'address', 'location',)


class BusRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusRating
        fields = ('Bus', 'user', 'rate',)


class BusSerializer(serializers.ModelSerializer):
    address = BusAddressSerializer()
    rate = BusRateSerializer(required=False)
    type = TransportTypeSerializer()

    class Meta:
        model = Bus
        fields = ('driver', 'description', 'type', 'status', 'max_reservation', 'number_reserved', 'source',
                  'destination',)

    def create(self, validated_data):
        source = validated_data.pop('source') if 'source' in validated_data else None
        destination = validated_data.pop('destination') if 'destination' in validated_data else None
        type = validated_data.pop('type') if 'type' in validated_data else None

        source = BusAddress.objects.create(**source)
        destination = BusAddress.objects.create(**destination)

        type, _ = TransportType.objects.get_or_create(title=type['title'], defaults={"title": type['title']})

        bus = Bus.objects.create(source=source, destination=destination, type=type, **validated_data)

        return bus
