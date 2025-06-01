from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    def has_module_permission(self, request):
        if request.user.is_api_user:
            return False
        return super().has_module_permission(request)


admin.site.register(User, CustomUserAdmin)
