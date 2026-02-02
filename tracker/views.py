"""
Tracker app views.
Handles study progress tracking and saving study sessions.
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from .models import StudySession
from rooms.models import Room


@login_required
def progress_view(request):
    """
    Display user's study progress and statistics.
    Shows today's total, this week's total, and last 7 days breakdown.
    """
    user = request.user
    now = timezone.now()
    today = now.date()
    
    # Calculate today's total minutes
    today_sessions = StudySession.objects.filter(
        user=user,
        created_at__date=today
    )
    today_total = today_sessions.aggregate(Sum('minutes'))['minutes__sum'] or 0
    
    # Calculate this week's total minutes
    week_start = today - timedelta(days=today.weekday())  # Monday of current week
    week_sessions = StudySession.objects.filter(
        user=user,
        created_at__date__gte=week_start
    )
    week_total = week_sessions.aggregate(Sum('minutes'))['minutes__sum'] or 0
    
    # Get last 7 days data for chart
    last_7_days = []
    for i in range(6, -1, -1):  # 6 days ago to today
        day = today - timedelta(days=i)
        day_sessions = StudySession.objects.filter(
            user=user,
            created_at__date=day
        )
        day_total = day_sessions.aggregate(Sum('minutes'))['minutes__sum'] or 0
        last_7_days.append({
            'date': day.strftime('%a'),  # Mon, Tue, etc.
            'minutes': day_total
        })
    
    # Get recent sessions for display
    recent_sessions = StudySession.objects.filter(user=user)[:10]
    
    context = {
        'today_total': today_total,
        'week_total': week_total,
        'last_7_days': last_7_days,
        'recent_sessions': recent_sessions,
    }
    return render(request, 'tracker/progress.html', context)


@login_required
def save_session_view(request):
    """
    Save a completed study session.
    Called via POST when Pomodoro timer completes.
    """
    if request.method == 'POST':
        minutes = request.POST.get('minutes')
        room_code = request.POST.get('room_code', '')
        
        try:
            minutes = int(minutes)
            if minutes <= 0:
                raise ValueError("Minutes must be positive")
            
            # Get room if room_code provided
            room = None
            if room_code:
                try:
                    room = Room.objects.get(room_code=room_code)
                except Room.DoesNotExist:
                    pass
            
            # Create study session
            session = StudySession.objects.create(
                user=request.user,
                room=room,
                minutes=minutes,
                ended_at=timezone.now()
            )
            
            # Update user profile stats (study streak and total minutes)
            user_profile = request.user.profile
            user_profile.update_study_stats(minutes)
            
            # Check for study milestones and create notifications
            from notifications.models import Notification
            Notification.create_study_milestone(request.user, user_profile.total_study_minutes)
            
            messages.success(request, f'Study session of {minutes} minutes saved!')
        
        except (ValueError, TypeError):
            messages.error(request, 'Invalid minutes value.')
        
        # Redirect back to room or progress page
        if room_code:
            return redirect('room_detail', room_code=room_code)
        return redirect('progress')
    
    return redirect('home')
