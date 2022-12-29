from django.db import transaction
from rest_framework import serializers

from reservations.models import Payment
from reservations.sub_models.location import Location
from reservations.sub_models.price import Price, Currency, CurrencyExchangeRate
from utlis.get_or_create_currency import get_or_create_currency


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'x_coordination', 'y_coordination',)


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id', 'user', 'payment_status', 'reserved_key',)


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ('id', 'name', 'code',)


class PriceByIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ('id', 'currency', 'value', 'from_date', 'to_date', 'ratio',)


class PriceByCurrencySerializer(serializers.ModelSerializer):
    currency = CurrencySerializer(many=False)

    class Meta:
        model = Price
        fields = ('id', 'currency', 'value', 'from_date', 'to_date', 'ratio',)

    @transaction.atomic
    def create(self, validated_data):
        currency = validated_data.pop('currency', None)

        currency, _ = get_or_create_currency(currency)

        price = Price.objects.create(currency=currency, **validated_data)
        return price

    @transaction.atomic
    def update(self, instance, validated_data):
        currency = validated_data.pop('currency', None)

        if currency:
            currency, _ = get_or_create_currency(currency)

            instance.currency = currency

        instance.value = validated_data.get('value', instance.value)
        instance.save()
        return instance


class CurrencyExchangeRateByIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyExchangeRate
        fields = ('id', 'rate', 'currency_from', 'currency_to',)


class CurrencyExchangeRateByCurrencySerializer(serializers.ModelSerializer):
    currency_from = CurrencySerializer(many=False)
    currency_to = CurrencySerializer(many=False)

    class Meta:
        model = CurrencyExchangeRate
        fields = ('id', 'rate', 'currency_from', 'currency_to',)

    @transaction.atomic
    def create(self, validated_data):
        currency_from = validated_data.pop('currency_from', None)
        currency_to = validated_data.pop('currency_to', None)

        currency_from, _ = get_or_create_currency(currency_from)
        currency_to, _ = get_or_create_currency(currency_to)

        ex, _ = CurrencyExchangeRate.objects.update_or_create(currency_from=currency_from, currency_to=currency_to,
                                                              defaults={"rate": validated_data['rate']})
        return ex

    @transaction.atomic
    def update(self, instance, validated_data):
        currency_from = validated_data.pop('currency_from', None)
        currency_to = validated_data.pop('currency_to', None)

        if currency_from:
            currency_from, _ = get_or_create_currency(currency_from)

            instance.currency_from = currency_from
        if currency_to:
            currency_to, _ = get_or_create_currency(currency_to)

            instance.currency_to = currency_to

        instance.rate = validated_data.get('rate', instance.rate)
        instance.save()
        return instance
