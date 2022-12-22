from django.urls import path, include
from rest_framework.routers import DefaultRouter

from reservations.views import *

router = DefaultRouter()
router.register(r'location', LocationViewSet, basename="location")
router.register(r'residence-type', ResidenceTypeViewSet, basename="residence-type")
router.register(r'transport-type', TransportTypeViewSet, basename="transport-type")
router.register(r'currency', CurrencyViewSet, basename="currency")
router.register(r'price', PriceViewSet, basename="price")
router.register(r'currency-exchange-rate', CurrencyExchangeRateViewSet, basename="currency-exchange-rate")

urlpatterns = [
    path('', include(router.urls)),
]
