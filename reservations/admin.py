from django.contrib import admin

from reservations.sub_models.location import Location
from reservations.sub_models.price import Currency, CurrencyExchangeRate, Price
from reservations.sub_models.type import ResidenceType, TransportType


class LocationAdmin(admin.ModelAdmin):
    pass


class CurrencyAdmin(admin.ModelAdmin):
    pass


class PriceAdmin(admin.ModelAdmin):
    pass


class CurrencyExchangeRateAdmin(admin.ModelAdmin):
    pass


class ResidenceTypeAdmin(admin.ModelAdmin):
    pass


class TransportTypeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Price, PriceAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(ResidenceType, ResidenceTypeAdmin)
admin.site.register(TransportType, TransportTypeAdmin)
admin.site.register(CurrencyExchangeRate, CurrencyExchangeRateAdmin)
