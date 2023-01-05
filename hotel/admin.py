from django.contrib import admin

from hotel.models import *


class HotelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'residence_status', 'price_per_night'
                    , 'star', 'room_count', 'is_valid')
    search_fields = ('name', 'star', 'residence_status')
    list_filter = ('is_valid', 'residence_status', 'star')


class HotelRoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'capacity', 'status', 'price', 'hotel')
    search_fields = ('name', 'hotel__name')
    list_filter = ('status', 'capacity',)


class HotelRatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'rate', 'hotel', 'is_valid')
    search_fields = ('hotel__name',)
    list_filter = ('user', 'rate', 'hotel')


class HotelCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'hotel',)
    search_fields = ('hotel',)
    list_filter = ('status',)

    def save_model(self, request, obj, form, change):
        if change and not obj.validated_by and 'status' in form.changed_data:
            obj.validated_by = request.user

        obj.save()


class HotelPassengerAdmin(admin.ModelAdmin):
    list_display = ('id', 'national_id', 'room', 'stay_status', 'reserved_key', 'parent')
    search_fields = ('national_id', 'reserved_key', 'room__number', 'room__hotel__name')
    list_filter = ('stay_status', 'room__hotel__name')


class HotelReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'room', 'check_in_date', 'check_out_date', 'reserved_key',)
    search_fields = ('reserved_key', 'room__number')
    list_filter = ('room__hotel__name', 'reserved_status')


class HotelAddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'country', 'city', 'phone')
    search_fields = ('country', 'city')
    list_filter = ('country', 'city')


class HotelGalleryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'hotel', 'is_valid')
    search_fields = ('name', 'hotel__name')
    list_filter = ('hotel', 'is_valid')


class HotelImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'gallery', 'is_main')
    search_fields = ['gallery__name']
    list_filter = ('is_main', 'gallery__hotel', 'gallery')


admin.site.register(Hotel, HotelAdmin)
admin.site.register(HotelRoom, HotelRoomAdmin)
admin.site.register(HotelRating, HotelRatingAdmin)
admin.site.register(HotelComment, HotelCommentAdmin)
admin.site.register(HotelPassenger, HotelPassengerAdmin)
admin.site.register(HotelReservation, HotelReservationAdmin)
admin.site.register(HotelAddress, HotelAddressAdmin)
admin.site.register(HotelGallery, HotelGalleryAdmin)
admin.site.register(HotelImage, HotelImageAdmin)
