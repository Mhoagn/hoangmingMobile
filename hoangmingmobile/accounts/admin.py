from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'full_name', 'role', 'is_active']
    list_editable = ['role']  # đổi role trực tiếp trên danh sách
    ordering = ['email']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Thông tin', {'fields': ('full_name', 'phone_number', 'role')}),
        ('Quyền hạn', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'fields': ('email', 'full_name', 'password1', 'password2', 'role'),
        }),
    )
    search_fields = ['email', 'full_name']
    filter_horizontal = ()