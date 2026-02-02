"""
Admin configuration for chat app.
"""
from django.contrib import admin
from .models import ChatMessage


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    """
    Admin interface for ChatMessage model.
    """
    list_display = ['user', 'room', 'message', 'timestamp']
    list_filter = ['timestamp', 'room']
    search_fields = ['user__username', 'room__name', 'message']
    readonly_fields = ['timestamp']
