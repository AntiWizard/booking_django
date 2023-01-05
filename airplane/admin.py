from django.contrib import admin

from airplane.models import *


class AirplaneAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'transport_status'
                    , 'transport_number', 'max_reservation', 'number_reserved')
    search_fields = ('company__airport_terminal__airport__title', 'transport_number')
    list_filter = ('transport_status',)


class AirplaneSeatAdmin(admin.ModelAdmin):
    list_display = ('id', 'airplane', 'number', 'status', 'price',)
    search_fields = ('airplane__company__airport_terminal__airport__title', 'number')
    list_filter = ('status',)


class AirplaneCompanyRatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'rate', 'company', 'is_valid')
    search_fields = ('company__name',)
    list_filter = ('user', 'rate', 'company__airport_terminal__airport__title')


class AirplaneCompanyCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'company',)
    search_fields = ('company__name',)
    list_filter = ('status',)

    def save_model(self, request, obj, form, change):
        if change and not obj.validated_by and 'status' in form.changed_data:
            obj.validated_by = request.user

        obj.save()


class AirplanePassengerAdmin(admin.ModelAdmin):
    list_display = ('id', 'national_id', 'seat', 'transfer_status', 'reserved_key', 'parent')
    search_fields = ('national_id', 'reserved_key', 'seat__number',
                     'seat__airplane__company__airport_terminal__airport__title')
    list_filter = ('transfer_status',)


class AirplaneReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'airplane', 'reserved_key',)
    search_fields = ('reserved_key',)
    list_filter = ('airplane__company__airport_terminal__airport__title',
                   'reserved_status')


class AirportAddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'country', 'city', 'phone')
    search_fields = ('country', 'city')
    list_filter = ('country', 'city')


admin.site.register(Airplane, AirplaneAdmin)
admin.site.register(AirplaneSeat, AirplaneSeatAdmin)
admin.site.register(AirplaneCompanyRating, AirplaneCompanyRatingAdmin)
admin.site.register(AirplaneCompanyComment, AirplaneCompanyCommentAdmin)
admin.site.register(AirplanePassenger, AirplanePassengerAdmin)
admin.site.register(AirplaneReservation, AirplaneReservationAdmin)
admin.site.register(AirportAddress, AirportAddressAdmin)
