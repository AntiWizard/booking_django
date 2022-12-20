from rest_framework import serializers

from reservations.sub_models.location import Location
from reservations.sub_models.price import Price, Currency
from reservations.sub_models.type import PlaceType, TransportType


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('x_coordination', 'y_coordination',)


class PlaceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceType
        fields = ('title',)


class TransportTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportType
        fields = ('title',)


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ('name', 'code',)


class PriceSerializer(serializers.ModelSerializer):
    currency = CurrencySerializer(required=False, read_only=True)

    class Meta:
        model = Price
        fields = ('currency', 'value',)


class CurrencyExchangeSerializer(serializers.ModelSerializer):
    currency_from = CurrencySerializer(required=False, read_only=True)
    currenc_to = CurrencySerializer(required=False, read_only=True)

    class Meta:
        model = Price
        fields = ('rate', 'currency_from', 'currency_to',)
