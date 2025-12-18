from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'favorite_team', 'is_staff', 'created_at']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'favorite_team']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-created_at']

    fieldsets = UserAdmin.fieldsets + (
        ('GridIron Preferences', {
            'fields': ('favorite_team', 'theme_preference', 'dark_mode')
        }),
        ('AI Assistant Settings', {
            'fields': ('ai_risk_tolerance', 'ai_prioritize_matchups', 'ai_consider_injuries')
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('GridIron Preferences', {
            'fields': ('email', 'favorite_team', 'theme_preference')
        }),
    )
