# from django.db import transaction
# from rest_framework import serializers, exceptions
#
# from airplane.models import Airplane, AirplaneAddress, AirplaneRating, AirplaneSeat
# from reservations.serializers import LocationSerializer, PriceByCurrencySerializer
# from reservations.sub_models.price import Currency, Price
#
#
# class AirplaneAddressSerializer(serializers.ModelSerializer):
#     location = LocationSerializer(required=False)
#
#     class Meta:
#         model = AirplaneAddress
#         fields = ('id', 'phone', 'country', 'city', 'address', 'location',)
#         extra_kwargs = {'phone': {'required': False}}
#
#
# class AirplaneRateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AirplaneRating
#         fields = ('id', 'airplane', 'user', 'rate',)
#
#
# class AirplaneSerializer(serializers.ModelSerializer):
#     source = AirplaneAddressSerializer()
#     destination = AirplaneAddressSerializer()
#
#     class Meta:
#         model = Airplane
#         fields = (
#             'id', 'transport_number', 'pilot', 'description', 'transport_status', 'max_reservation', 'number_reserved',
#             'source', 'destination', 'transfer_date',)
#         extra_kwargs = {"transport_number": {"required": False, "read_only": True}}
#
#     @transaction.atomic
#     def create(self, validated_data):
#         source = validated_data.pop('source', None)
#         destination = validated_data.pop('destination', None)
#
#         try:
#             source = AirplaneAddress.objects.create(**source)
#             destination = AirplaneAddress.objects.create(**destination)
#         except Exception:
#             raise exceptions.ValidationError("invalid address")
#
#         airplane = Airplane.objects.create(source=source, destination=destination, **validated_data)
#         return airplane
#
#     @transaction.atomic
#     def update(self, instance, validated_data):
#         source = validated_data.pop('source', None)
#         destination = validated_data.pop('destination', None)
#
#         try:
#             for attr, value in validated_data.items():
#                 setattr(instance, attr, value)
#         except Exception:
#             raise exceptions.ValidationError("invalid data")
#
#         instance.save()
#
#         if source:
#             source_address = AirplaneAddress.objects.filter(phone=instance.source.phone).get()
#             try:
#                 for attr, value in source.items():
#                     setattr(source_address, attr, value)
#             except Exception:
#                 raise exceptions.ValidationError("invalid data")
#             source_address.save()
#             instance.source = source_address
#
#         if destination:
#             destination_address = AirplaneAddress.objects.filter(phone=instance.source.phone).get()
#             try:
#                 for attr, value in source.items():
#                     setattr(destination_address, attr, value)
#             except Exception:
#                 raise exceptions.ValidationError("invalid data")
#             destination_address.save()
#             instance.destination = destination_address
#
#         return instance
#
#
# class AirplaneSeatSerializer(serializers.ModelSerializer):
#     price = PriceByCurrencySerializer()
#
#     class Meta:
#         model = AirplaneSeat
#         fields = ('id', 'number', 'status', 'price', 'airplane')
#
#     @transaction.atomic
#     def create(self, validated_data):
#         price = validated_data.pop('price', None)
#         currency = price.pop('currency', None)
#
#         try:
#             currency, _ = Currency.objects.get_or_create(name=currency.get('name', None),
#                                                          defaults={"code": currency.get('code', None)})
#             price = Price.objects.create(currency=currency, **price)
#         except Exception:
#             raise exceptions.ValidationError("invalid data")
#
#         airplane_seat = AirplaneSeat.objects.create(price=price, **validated_data)
#
#         return airplane_seat
#
#     @transaction.atomic
#     def update(self, instance, validated_data):
#         price_seat = validated_data.pop('price', None)
#         currency = price_seat.pop('currency', None)
#
#         try:
#             for attr, value in validated_data.items():
#                 setattr(instance, attr, value)
#         except AirplaneSeat.DoesNotExist:
#             raise exceptions.ValidationError("invalid data")
#
#         instance.save()
#
#         if price_seat:
#             if currency:
#                 currency_room = Currency.objects.filter(id=instance.price.currency.id).get()
#                 try:
#                     for attr, value in currency.items():
#                         setattr(currency_room, attr, value)
#                 except Currency.DoesNotExist:
#                     raise exceptions.ValidationError("invalid data")
#                 currency_room.save()
#
#             price = Price.objects.filter(id=instance.price_per_night.id).get()
#             try:
#                 for attr, value in price_seat.items():
#                     setattr(price, attr, value)
#             except Price.DoesNotExist:
#                 raise exceptions.ValidationError("invalid data")
#             price.save()
#             instance.price = price
#
#         return instance
