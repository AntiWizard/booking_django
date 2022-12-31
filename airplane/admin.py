from django.contrib import admin

from airplane.models import Airplane, AirplaneReservation, AirplaneSeat, AirportCompanyRating


class AirplaneAdmin(admin.ModelAdmin):
    pass


class AirplaneSeatAdmin(admin.ModelAdmin):
    pass


class AirplaneReservationAdmin(admin.ModelAdmin):
    pass


class AirportCompanyRatingAdmin(admin.ModelAdmin):
    pass


admin.site.register(Airplane, AirplaneAdmin)
admin.site.register(AirplaneSeat, AirplaneSeatAdmin)
admin.site.register(AirplaneReservation, AirplaneReservationAdmin)
admin.site.register(AirportCompanyRating, AirportCompanyRatingAdmin)
