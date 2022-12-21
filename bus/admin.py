from django.contrib import admin

from bus.models import Bus, BusReservation, BusSeat, BusAddress, BusRating


class BusAdmin(admin.ModelAdmin):
    pass


class BusSeatAdmin(admin.ModelAdmin):
    pass


class BusReservationAdmin(admin.ModelAdmin):
    pass


class BusRatingAdmin(admin.ModelAdmin):
    pass


class BusAddressAdmin(admin.ModelAdmin):
    pass


admin.site.register(Bus, BusAdmin)
admin.site.register(BusSeat, BusSeatAdmin)
admin.site.register(BusReservation, BusReservationAdmin)
admin.site.register(BusRating, BusRatingAdmin)
admin.site.register(BusAddress, BusAddressAdmin)
