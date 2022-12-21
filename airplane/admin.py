from django.contrib import admin

from airplane.models import Airplane, AirplaneReservation, AirplaneSeat, AirplaneAddress, AirplaneRating


class AirplaneAdmin(admin.ModelAdmin):
    pass


class AirplaneSeatAdmin(admin.ModelAdmin):
    pass


class AirplaneReservationAdmin(admin.ModelAdmin):
    pass


class AirplaneRatingAdmin(admin.ModelAdmin):
    pass


class AirplaneAddressAdmin(admin.ModelAdmin):
    pass


admin.site.register(Airplane, AirplaneAdmin)
admin.site.register(AirplaneSeat, AirplaneSeatAdmin)
admin.site.register(AirplaneReservation, AirplaneReservationAdmin)
admin.site.register(AirplaneRating, AirplaneRatingAdmin)
admin.site.register(AirplaneAddress, AirplaneAddressAdmin)
