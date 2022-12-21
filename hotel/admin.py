from django.contrib import admin

from hotel.models import Hotel, HotelReservation, HotelRoom, HotelAddress, HotelRating


class HotelAdmin(admin.ModelAdmin):
    pass


class HotelRoomAdmin(admin.ModelAdmin):
    pass


class HotelReservationAdmin(admin.ModelAdmin):
    pass


class HotelRatingAdmin(admin.ModelAdmin):
    pass


class HotelAddressAdmin(admin.ModelAdmin):
    pass


admin.site.register(Hotel, HotelAdmin)
admin.site.register(HotelRoom, HotelRoomAdmin)
admin.site.register(HotelReservation, HotelReservationAdmin)
admin.site.register(HotelRating, HotelRatingAdmin)
admin.site.register(HotelAddress, HotelAddressAdmin)
