"""
Rooms app views.
Handles room listing, creation, and detail pages.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta
from .models import Room, RoomMembership


def landing_view(request):
    """
    Landing page for non-authenticated users.
    Shows intro to Virtual Cafe with call to action.
    """
    # If user is already logged in, redirect to dashboard
    if request.user.is_authenticated:
        return redirect('home')
    
    return render(request, 'landing.html')


@login_required
def home_view(request):
    """
    Home dashboard showing rooms created by the current user.
    Users must be logged in to see this page.
    """
    # Clean up expired rooms (excluding the global room)
    expired_rooms = Room.objects.filter(
        expires_at__lte=timezone.now()
    ).exclude(room_code='GLOBAL')
    expired_count = expired_rooms.count()
    if expired_count > 0:
        expired_rooms.delete()
        messages.info(request, f'{expired_count} empty room(s) expired and removed.')
    
    # Get all active PUBLIC rooms created by the current user
    rooms = Room.objects.filter(
        Q(expires_at__isnull=True) | Q(expires_at__gt=timezone.now()),
        is_public=True,
        created_by=request.user  # Only show rooms created by current user
    )
    
    # Get search query from GET parameters
    search_query = request.GET.get('search', '').strip()
    
    # Apply search filter if provided
    if search_query:
        # Search in room name and description
        rooms = rooms.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Annotate with member count for display
    rooms = rooms.annotate(
        member_count=Count('memberships', filter=Q(memberships__is_active=True))
    ).select_related('created_by')
    
    # Get rooms the current user is a member of
    user_rooms = Room.objects.filter(memberships__user=request.user, memberships__is_active=True)
    
    context = {
        'rooms': rooms,
        'user_rooms': user_rooms,
        'search_query': search_query,
    }
    return render(request, 'rooms/home.html', context)


@login_required
def create_room_view(request):
    """
    Create a new study room.
    GET: Display create room form
    POST: Create the room and redirect to room detail
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        is_public = request.POST.get('is_public') == 'on'  # Checkbox value
        
        # Validate room name
        if not name or len(name.strip()) == 0:
            messages.error(request, 'Room name is required.')
            return render(request, 'rooms/create_room.html')
        
        # Create the room
        room = Room.objects.create(
            name=name,
            description=description,
            created_by=request.user,
            is_public=is_public
        )
        
        # Automatically add creator as a member
        RoomMembership.objects.create(
            user=request.user,
            room=room,
            is_active=True
        )
        
        visibility = "public" if is_public else "private"
        messages.success(request, f'Room "{name}" created successfully as {visibility}!')
        return redirect('room_detail', room_code=room.room_code)
    
    # GET request - show form
    return render(request, 'rooms/create_room.html')


@login_required
def global_chat_view(request):
    """
    Global chat room where anyone can join and chat with everyone.
    Requires the global room to be created first.
    """
    # Try to get the global chat room (do not auto-create)
    try:
        global_room = Room.objects.get(room_code='GLOBAL')
    except Room.DoesNotExist:
        messages.error(request, 'Global chat room has not been created yet. Please contact administrator.')
        return redirect('home')
    
    # Check if user is already a member
    existing_membership = RoomMembership.objects.filter(
        user=request.user,
        room=global_room
    ).first()
    
    # If already a member, reactivate if needed
    if existing_membership:
        if not existing_membership.is_active:
            existing_membership.is_active = True
            existing_membership.save()
    else:
        # Create new membership
        RoomMembership.objects.create(
            user=request.user,
            room=global_room,
            is_active=True
        )
    
    # Update room activity
    global_room.update_activity()
    
    # Get all active members in the room
    active_members = RoomMembership.objects.filter(
        room=global_room,
        is_active=True
    ).select_related('user')
    
    context = {
        'room': global_room,
        'active_members': active_members,
        'members_count': active_members.count(),
        'is_owner': global_room.created_by == request.user,
        'is_global': True,  # Flag to indicate this is the global room
    }
    return render(request, 'rooms/chat_room.html', context)


@login_required
def join_room_by_code_view(request):
    """
    Handle joining a room by entering a room code.
    GET: Display join room form
    POST: Join the room by code and redirect to room detail
    """
    if request.method == 'POST':
        room_code = request.POST.get('room_code', '').strip().upper()
        
        # Validate room code
        if not room_code:
            messages.error(request, 'Please enter a room code.')
            return redirect('home')
        
        # Try to find the room
        try:
            room = Room.objects.get(room_code=room_code)
            
            # Check if room has expired
            if room.is_expired():
                room.delete()
                messages.error(request, 'This room has expired due to inactivity.')
                return redirect('home')
            
            # Redirect to room detail (which handles membership creation)
            messages.success(request, f'Joining room "{room.name}"...')
            return redirect('room_detail', room_code=room.room_code)
            
        except Room.DoesNotExist:
            messages.error(request, f'Room with code "{room_code}" not found. Please check the code and try again.')
            return redirect('home')
    
    # GET request - redirect to home
    return redirect('home')


@login_required
def room_detail_view(request, room_code):
    """
    Room detail page with chat, video call, timer, and members list.
    This is the main study room interface.
    Checks room capacity and permissions before allowing entry.
    """
    # Get the room or return 404 if not found
    room = get_object_or_404(Room, room_code=room_code)
    
    # Check if room has expired
    if room.is_expired():
        room.delete()
        messages.error(request, 'This room has expired due to inactivity.')
        return redirect('home')
    
    # Check if user is already a member
    existing_membership = RoomMembership.objects.filter(
        user=request.user,
        room=room
    ).first()
    
    # If already a member, reactivate if needed
    if existing_membership:
        if not existing_membership.is_active:
            existing_membership.is_active = True
            existing_membership.save()
    else:
        # Create new membership
        RoomMembership.objects.create(
            user=request.user,
            room=room,
            is_active=True
        )
        
        # Create notification for room owner (if not the owner joining)
        if room.created_by != request.user:
            from notifications.models import Notification
            Notification.create_new_member_notification(
                room_owner=room.created_by,
                new_member=request.user,
                room=room
            )
    
    # Update room activity (clears expiration since user just joined)
    room.update_activity()
    
    # Get all active members in the room
    active_members = RoomMembership.objects.filter(
        room=room,
        is_active=True
    ).select_related('user')
    
    context = {
        'room': room,
        'active_members': active_members,
        'members_count': active_members.count(),
        'is_owner': room.created_by == request.user,
    }
    return render(request, 'rooms/room_detail.html', context)
