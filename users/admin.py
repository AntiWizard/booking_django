from django.contrib import admin

from users.models import User, Address


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone', 'is_active', 'is_staff',)
    search_fields = ('phone',)


class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone',)
    search_fields = ('phone',)


admin.site.register(User, UserAdmin)
admin.site.register(Address, AddressAdmin)
