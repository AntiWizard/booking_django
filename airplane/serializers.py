from django.db import transaction
from rest_framework import serializers, exceptions

from airplane.models import *
from reservations.base_models.comment import CommentStatus
from reservations.serializers import LocationSerializer, PriceByCurrencySerializer
from reservations.sub_models.price import Currency, Price


# ---------------------------------------------Airport------------------------------------------------------------------

class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ('id', 'title', 'address',)


class AirportTerminalSerializer(serializers.ModelSerializer):
    # airplane = AirportSerializer

    class Meta:
        model = AirportTerminal
        fields = ('id', 'number', 'airport',)


class AirportTerminalCompanySerializer(serializers.ModelSerializer):
    # airport_terminal = AirportTerminalSerializer

    class Meta:
        model = AirportTerminalCompany
        fields = ('id', 'name', 'airport_terminal',)


# ---------------------------------------------AirportAddress-----------------------------------------------------------

class AirportAddressSerializer(serializers.ModelSerializer):
    location = LocationSerializer(required=False)

    class Meta:
        model = AirportAddress
        fields = ('id', 'phone', 'country', 'city', 'address', 'location', 'zip_code',)
        extra_kwargs = {'phone': {'required': False}}


# ---------------------------------------------AirportCompanyRating-----------------------------------------------------

class AirportCompanyRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirportCompanyRating
        fields = ('id', 'company', 'user', 'rate',)


# ---------------------------------------------AirplaneCompanyComment----------------------------------------------------

class AirplaneCompanyCommentForCreatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneCompanyComment
        fields = ('id', 'company', 'user', 'status', 'parent', 'comment_body', 'validated_by')
        extra_kwargs = {"parent": {"required": False}}


class AirplaneCompanyCommentUpdatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneCompanyComment
        fields = ('id', 'status', 'comment_body', 'validated_by')
        extra_kwargs = {"validated_by": {"required": False, "read_only": True}}

    def update(self, instance, validated_data):
        if instance.status not in [CommentStatus.CREATED]:
            raise exceptions.ValidationError("Comment with result cant be update")

        if instance.comment_body == validated_data['comment_body']:
            return instance

        try:
            instance.comment_body = validated_data['comment_body']
            instance.validated_by = None

        except (ValueError, TypeError) as e:
            raise exceptions.ValidationError("invalid data -> {}".format(e))

        instance.save()

        return instance


# ---------------------------------------------AirportCompanyRating-----------------------------------------------------


class AirplaneSerializer(serializers.ModelSerializer):
    # source = AirportAddressSerializer()
    # destination = AirportAddressSerializer()
    # company = AirportTerminalCompanySerializer()

    class Meta:
        model = Airplane
        fields = (
            'id', 'pilot', 'company', 'transport_number', 'description', 'transport_status', 'max_reservation',
            'number_reserved', 'duration', 'destination', 'transfer_date',)
        extra_kwargs = {"transport_number": {"required": False, "read_only": True}}

    @transaction.atomic
    def create(self, validated_data):
        source = validated_data.pop('source', None)
        destination = validated_data.pop('destination', None)

        try:
            source = AirportAddress.objects.create(**source)
            destination = AirportAddress.objects.create(**destination)
        except Exception:
            raise exceptions.ValidationError("invalid address")

        airplane = Airplane.objects.create(source=source, destination=destination, **validated_data)
        return airplane

    @transaction.atomic
    def update(self, instance, validated_data):
        source = validated_data.pop('source', None)
        destination = validated_data.pop('destination', None)

        try:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
        except Exception:
            raise exceptions.ValidationError("invalid data")

        instance.save()

        if source:
            source_address = AirportAddress.objects.filter(phone=instance.source.phone).get()
            try:
                for attr, value in source.items():
                    setattr(source_address, attr, value)
            except Exception:
                raise exceptions.ValidationError("invalid data")
            source_address.save()
            instance.source = source_address

        if destination:
            destination_address = AirportAddress.objects.filter(phone=instance.source.phone).get()
            try:
                for attr, value in source.items():
                    setattr(destination_address, attr, value)
            except Exception:
                raise exceptions.ValidationError("invalid data")
            destination_address.save()
            instance.destination = destination_address

        return instance


# ---------------------------------------------AirportSeat--------------------------------------------------------------

class AirplaneSeatSerializer(serializers.ModelSerializer):
    price = PriceByCurrencySerializer()

    class Meta:
        model = AirplaneSeat
        fields = ('id', 'number', 'status', 'price', 'airplane')

    @transaction.atomic
    def create(self, validated_data):
        price = validated_data.pop('price', None)
        currency = price.pop('currency', None)

        try:
            currency, _ = Currency.objects.get_or_create(name=currency.get('name', None),
                                                         defaults={"code": currency.get('code', None)})
            price = Price.objects.create(currency=currency, **price)
        except Exception:
            raise exceptions.ValidationError("invalid data")

        airplane_seat = AirplaneSeat.objects.create(price=price, **validated_data)

        return airplane_seat

    @transaction.atomic
    def update(self, instance, validated_data):
        price_seat = validated_data.pop('price', None)
        currency = price_seat.pop('currency', None)

        try:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
        except AirplaneSeat.DoesNotExist:
            raise exceptions.ValidationError("invalid data")

        instance.save()

        if price_seat:
            if currency:
                currency_room = Currency.objects.filter(id=instance.price.currency.id).get()
                try:
                    for attr, value in currency.items():
                        setattr(currency_room, attr, value)
                except Currency.DoesNotExist:
                    raise exceptions.ValidationError("invalid data")
                currency_room.save()

            price = Price.objects.filter(id=instance.price_per_night.id).get()
            try:
                for attr, value in price_seat.items():
                    setattr(price, attr, value)
            except Price.DoesNotExist:
                raise exceptions.ValidationError("invalid data")
            price.save()
            instance.price = price

        return instance
