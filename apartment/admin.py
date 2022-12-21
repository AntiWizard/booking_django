from django.contrib import admin

from apartment.models import Apartment, ApartmentReservation, ApartmentRoom, ApartmentAddress, ApartmentRating


class ApartmentAdmin(admin.ModelAdmin):
    pass


class ApartmentRoomAdmin(admin.ModelAdmin):
    pass


class ApartmentReservationAdmin(admin.ModelAdmin):
    pass


class ApartmentRatingAdmin(admin.ModelAdmin):
    pass


class ApartmentAddressAdmin(admin.ModelAdmin):
    pass


admin.site.register(Apartment, ApartmentAdmin)
admin.site.register(ApartmentRoom, ApartmentRoomAdmin)
admin.site.register(ApartmentReservation, ApartmentReservationAdmin)
admin.site.register(ApartmentRating, ApartmentRatingAdmin)
admin.site.register(ApartmentAddress, ApartmentAddressAdmin)
