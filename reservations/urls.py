from django.urls import path, include
from rest_framework.routers import DefaultRouter

from reservations.views import *

router = DefaultRouter()
router.register(r'location', LocationViewSet, basename="location")
router.register(r'currency', CurrencyViewSet, basename="currency")
router.register(r'price/by-id', PriceByIdViewSet, basename="price")
router.register(r'price/by-currency', PriceByCurrencyViewSet, basename="price")
router.register(r'exchange-rate/by-id', CurrencyExchangeRateByIdViewSet, basename="currency-exchange-rate")
router.register(r'exchange-rate/by-currency', CurrencyExchangeRateByCurrencyViewSet, basename="currency-exchange-rate")

urlpatterns = [
    path('', include(router.urls)),
]
