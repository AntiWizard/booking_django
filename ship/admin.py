from django.contrib import admin

from ship.models import Ship, ShipReservation, ShipSeat, ShipAddress, ShipRating


class ShipAdmin(admin.ModelAdmin):
    pass


class ShipSeatAdmin(admin.ModelAdmin):
    pass


class ShipReservationAdmin(admin.ModelAdmin):
    pass


class ShipRatingAdmin(admin.ModelAdmin):
    pass


class ShipAddressAdmin(admin.ModelAdmin):
    pass


admin.site.register(Ship, ShipAdmin)
admin.site.register(ShipSeat, ShipSeatAdmin)
admin.site.register(ShipReservation, ShipReservationAdmin)
admin.site.register(ShipRating, ShipRatingAdmin)
admin.site.register(ShipAddress, ShipAddressAdmin)
