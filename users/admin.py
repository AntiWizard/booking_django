from django.contrib import admin

from users.models import User, UserAddress


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone', 'is_active', 'is_staff',)
    search_fields = ('phone',)
    list_filter = ('is_active',)

    def delete_queryset(self, request, queryset):
        UserAddress.objects.filter(phone__in=[item.phone for item in queryset]).delete()
        queryset.delete()


class UserAddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'country', 'city', 'phone',)
    search_fields = ('phone',)
    list_filter = ('country', 'city',)


admin.site.register(User, UserAdmin)
admin.site.register(UserAddress, UserAddressAdmin)
