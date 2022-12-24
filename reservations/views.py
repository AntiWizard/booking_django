from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication

from reservations.serializers import LocationSerializer, \
    CurrencySerializer, PriceByIdSerializer, PriceByCurrencySerializer, CurrencyExchangeRateByIdSerializer, \
    CurrencyExchangeRateByCurrencySerializer
from reservations.sub_models.location import Location
from reservations.sub_models.price import Currency, Price, CurrencyExchangeRate


class AbstractReservation(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    # pagination_class = [LimitOffsetPagination]


class LocationViewSet(AbstractReservation):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class CurrencyViewSet(AbstractReservation):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class PriceByIdViewSet(AbstractReservation):
    queryset = Price.objects.all()
    serializer_class = PriceByIdSerializer


class PriceByCurrencyViewSet(AbstractReservation):
    queryset = Price.objects.all()
    serializer_class = PriceByCurrencySerializer


class CurrencyExchangeRateByIdViewSet(AbstractReservation):
    queryset = CurrencyExchangeRate.objects.all()
    serializer_class = CurrencyExchangeRateByIdSerializer


class CurrencyExchangeRateByCurrencyViewSet(AbstractReservation):
    queryset = CurrencyExchangeRate.objects.all()
    serializer_class = CurrencyExchangeRateByCurrencySerializer
