"""
Chat app models.
Defines ChatMessage model for storing chat messages.
"""
from django.db import models
from django.contrib.auth.models import User
from rooms.models import Room


class ChatMessage(models.Model):
    """
    Represents a chat message sent in a room.
    """
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}: {self.message[:50]}"
    
    class Meta:
        ordering = ['timestamp']  # Oldest messages first
