"""
Admin configuration for user management.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom admin for User model."""

    # Fields displayed in the list view
    list_display = (
        'email', 'username', 'full_name', 'phone_number',
        'is_verified', 'is_staff', 'is_active', 'date_joined', 'avatar_preview'
    )

    # Available filters
    list_filter = (
        'is_staff', 'is_superuser', 'is_active', 'is_verified',
        'date_joined', 'last_login'
    )

    # Search fields
    search_fields = ('email', 'username', 'first_name', 'last_name', 'phone_number')

    # Default ordering
    ordering = ('-date_joined',)

    # Available actions
    actions = ['make_verified', 'make_unverified', 'activate_users', 'deactivate_users']

    # Fieldset configuration
    fieldsets = (
        (None, {
            'fields': ('email', 'username', 'password')
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'phone_number')
        }),
        ('Profile Picture', {
            'fields': ('avatar', 'avatar_preview_large'),
            'classes': ('collapse',)
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_verified',)
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )

    # Fieldsets for adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
        ('Personal Information', {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'phone_number'),
        }),
        ('Permissions', {
            'classes': ('collapse',),
            'fields': ('is_staff', 'is_superuser'),
        }),
    )

    # Read-only fields
    readonly_fields = ('date_joined', 'last_login', 'avatar_preview_large', 'created_at', 'updated_at')

    def avatar_preview(self, obj):
        """Small avatar preview in the list view."""
        if obj.avatar:
            return format_html(
                '<img src="{}" width="30" height="30" style="border-radius: 50%;" />',
                obj.avatar.url
            )
        return "No avatar"

    avatar_preview.short_description = 'Avatar'

    def avatar_preview_large(self, obj):
        """Large avatar preview in the form view."""
        if obj.avatar:
            return format_html(
                '<img src="{}" width="100" height="100" style="border-radius: 10px;" />',
                obj.avatar.url
            )
        return "No avatar"

    avatar_preview_large.short_description = 'Avatar Preview'

    def full_name(self, obj):
        """Display full name with icons for different user types."""
        name = obj.full_name
        if obj.is_superuser:
            return format_html(
                '<strong style="color: #e74c3c;">👑 {}</strong>',
                name
            )
        elif obj.is_staff:
            return format_html(
                '<strong style="color: #3498db;">🛠️ {}</strong>',
                name
            )
        elif obj.is_verified:
            return format_html(
                '<span style="color: #27ae60;">✅ {}</span>',
                name
            )
        return name

    full_name.short_description = 'Full Name'

    # Custom actions
    def make_verified(self, request, queryset):
        """Mark selected users as verified."""
        updated = queryset.update(is_verified=True)
        self.message_user(
            request,
            f'{updated} user(s) marked as verified.'
        )

    make_verified.short_description = 'Mark as verified'

    def make_unverified(self, request, queryset):
        """Mark selected users as unverified."""
        updated = queryset.update(is_verified=False)
        self.message_user(
            request,
            f'{updated} user(s) marked as unverified.'
        )

    make_unverified.short_description = 'Mark as unverified'

    def activate_users(self, request, queryset):
        """Activate selected users."""
        updated = queryset.update(is_active=True)
        self.message_user(
            request,
            f'{updated} user(s) activated.'
        )

    activate_users.short_description = 'Activate selected users'

    def deactivate_users(self, request, queryset):
        """Deactivate selected users."""
        updated = queryset.update(is_active=False)
        self.message_user(
            request,
            f'{updated} user(s) deactivated.'
        )

    deactivate_users.short_description = 'Deactivate selected users'


# Customize admin site
admin.site.site_header = 'Django Boilerplate Administration'
admin.site.site_title = 'Django Boilerplate Admin'
admin.site.index_title = 'Dashboard'