from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication

from reservations.serializers import LocationSerializer, ResidenceTypeSerializer, TransportTypeSerializer, \
    CurrencySerializer, PriceSerializer, CurrencyExchangeRateSerializer
from reservations.sub_models.location import Location
from reservations.sub_models.price import Currency, Price, CurrencyExchangeRate
from reservations.sub_models.type import ResidenceType, TransportType


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny]
        return [IsAdminUser]


class ResidenceTypeViewSet(viewsets.ModelViewSet):
    queryset = ResidenceType.objects.all()
    serializer_class = ResidenceTypeSerializer
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny]
        return [IsAdminUser]


class TransportTypeViewSet(viewsets.ModelViewSet):
    queryset = TransportType.objects.all()
    serializer_class = TransportTypeSerializer
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny]
        return [IsAdminUser]


class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny]
        return [IsAdminUser]


class PriceViewSet(viewsets.ModelViewSet):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny]
        return [IsAdminUser]


class CurrencyExchangeRateViewSet(viewsets.ModelViewSet):
    queryset = CurrencyExchangeRate.objects.all()
    serializer_class = CurrencyExchangeRateSerializer
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny]
        return [IsAdminUser]
