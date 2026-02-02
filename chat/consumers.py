"""
WebSocket Consumer for chat and WebRTC signaling.
Handles:
- Chat messages
- Join/leave notifications
- WebRTC signaling (offer, answer, ICE candidates)
- Pomodoro timer events (optional)
"""
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from .models import ChatMessage
from rooms.models import Room, RoomMembership


class RoomConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for handling room-related real-time events.
    Each room has its own channel group for broadcasting messages.
    """
    
    async def connect(self):
        """
        Called when WebSocket connection is established.
        Join the room's channel group.
        """
        # Get room code from URL
        self.room_code = self.scope['url_route']['kwargs']['room_code']
        # Create a unique group name for this room
        self.room_group_name = f'room_{self.room_code}'
        
        # Get user from scope (provided by AuthMiddlewareStack)
        self.user = self.scope['user']
        
        # Only allow authenticated users
        if not self.user.is_authenticated:
            await self.close()
            return
        
        # Join room group (all users in same room share this group)
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        # Accept WebSocket connection
        await self.accept()
        
        # Mark user as active in the room
        await self.set_user_active(True)
        
        # Send join notification to all users in the room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_join',
                'username': self.user.username
            }
        )
    
    async def disconnect(self, close_code):
        """
        Called when WebSocket connection is closed.
        Leave the room's channel group.
        """
        # Mark user as inactive in the room
        await self.set_user_active(False)
        
        # Send leave notification to all users in the room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_leave',
                'username': self.user.username
            }
        )
        
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        """
        Called when we receive a message from WebSocket.
        Parse the message and route to appropriate handler.
        """
        try:
            data = json.loads(text_data)
            message_type = data.get('type')
            
            # Route message based on type
            if message_type == 'chat':
                # Handle chat message
                await self.handle_chat_message(data)
            
            elif message_type == 'webrtc_offer':
                # Handle WebRTC offer for video call
                await self.handle_webrtc_offer(data)
            
            elif message_type == 'webrtc_answer':
                # Handle WebRTC answer
                await self.handle_webrtc_answer(data)
            
            elif message_type == 'webrtc_ice':
                # Handle ICE candidate for WebRTC connection
                await self.handle_webrtc_ice(data)
            
            elif message_type == 'timer':
                # Handle timer events (optional)
                await self.handle_timer_event(data)
        
        except json.JSONDecodeError:
            # Invalid JSON, ignore
            pass
    
    async def handle_chat_message(self, data):
        """
        Handle incoming chat message.
        Save to database and broadcast to all users in room.
        """
        message_text = data.get('message', '').strip()
        
        if not message_text:
            return
        
        # Save message to database
        await self.save_chat_message(message_text)
        
        # Broadcast message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_text,
                'username': self.user.username,
                'timestamp': timezone.now().isoformat()
            }
        )
    
    async def handle_webrtc_offer(self, data):
        """
        Handle WebRTC offer from one peer.
        Broadcast to all other users in the room (for 1-to-1, receiver will respond).
        """
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'webrtc_offer',
                'offer': data.get('offer'),
                'username': self.user.username
            }
        )
    
    async def handle_webrtc_answer(self, data):
        """
        Handle WebRTC answer from peer.
        Broadcast to all users in the room.
        """
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'webrtc_answer',
                'answer': data.get('answer'),
                'username': self.user.username
            }
        )
    
    async def handle_webrtc_ice(self, data):
        """
        Handle ICE candidate for WebRTC connection.
        Broadcast to all users in the room.
        """
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'webrtc_ice',
                'candidate': data.get('candidate'),
                'username': self.user.username
            }
        )
    
    async def handle_timer_event(self, data):
        """
        Handle Pomodoro timer events (optional).
        Broadcast timer state to all users in the room.
        """
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'timer_event',
                'action': data.get('action'),
                'minutes': data.get('minutes'),
                'username': self.user.username
            }
        )
    
    # Channel layer event handlers (called when group_send is used)
    
    async def chat_message(self, event):
        """
        Send chat message to WebSocket.
        """
        await self.send(text_data=json.dumps({
            'type': 'chat',
            'message': event['message'],
            'username': event['username'],
            'timestamp': event['timestamp']
        }))
    
    async def user_join(self, event):
        """
        Send join notification to WebSocket.
        """
        await self.send(text_data=json.dumps({
            'type': 'join',
            'username': event['username']
        }))
    
    async def user_leave(self, event):
        """
        Send leave notification to WebSocket.
        """
        await self.send(text_data=json.dumps({
            'type': 'leave',
            'username': event['username']
        }))
    
    async def webrtc_offer(self, event):
        """
        Send WebRTC offer to WebSocket.
        """
        # Don't send offer back to sender
        if event['username'] != self.user.username:
            await self.send(text_data=json.dumps({
                'type': 'webrtc_offer',
                'offer': event['offer'],
                'username': event['username']
            }))
    
    async def webrtc_answer(self, event):
        """
        Send WebRTC answer to WebSocket.
        """
        # Don't send answer back to sender
        if event['username'] != self.user.username:
            await self.send(text_data=json.dumps({
                'type': 'webrtc_answer',
                'answer': event['answer'],
                'username': event['username']
            }))
    
    async def webrtc_ice(self, event):
        """
        Send ICE candidate to WebSocket.
        """
        # Don't send ICE back to sender
        if event['username'] != self.user.username:
            await self.send(text_data=json.dumps({
                'type': 'webrtc_ice',
                'candidate': event['candidate'],
                'username': event['username']
            }))
    
    async def timer_event(self, event):
        """
        Send timer event to WebSocket.
        """
        await self.send(text_data=json.dumps({
            'type': 'timer',
            'action': event['action'],
            'minutes': event['minutes'],
            'username': event['username']
        }))
    
    # Database helper methods
    
    @database_sync_to_async
    def save_chat_message(self, message):
        """
        Save chat message to database.
        """
        try:
            room = Room.objects.get(room_code=self.room_code)
            ChatMessage.objects.create(
                room=room,
                user=self.user,
                message=message
            )
        except Room.DoesNotExist:
            pass
    
    @database_sync_to_async
    def set_user_active(self, is_active):
        """
        Mark user as active/inactive in the room.
        """
        try:
            room = Room.objects.get(room_code=self.room_code)
            membership, created = RoomMembership.objects.get_or_create(
                user=self.user,
                room=room
            )
            membership.is_active = is_active
            membership.save()
        except Room.DoesNotExist:
            pass
