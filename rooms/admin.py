"""
Admin configuration for rooms app.
Register Room and RoomMembership models in Django admin panel.
"""
from django.contrib import admin
from .models import Room, RoomMembership


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    """
    Admin interface for Room model.
    """
    list_display = ['name', 'room_code', 'created_by', 'created_at']
    search_fields = ['name', 'room_code', 'created_by__username', 'description']
    readonly_fields = ['room_code', 'created_at']
    
    fields = ('name', 'description', 'created_by', 'room_code', 'created_at')


@admin.register(RoomMembership)
class RoomMembershipAdmin(admin.ModelAdmin):
    """
    Admin interface for RoomMembership model.
    """
    list_display = ['user', 'room', 'joined_at', 'is_active']
    list_filter = ['is_active', 'joined_at']
    search_fields = ['user__username', 'room__name']

