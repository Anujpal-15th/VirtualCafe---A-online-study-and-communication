# solo/views.py
"""
Solo Study Room Views
The main study page where magic happens!
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.db.models import Sum
from datetime import datetime, timedelta
import json

from tracker.models import Task, StudySession, Achievement, UserAchievement
from accounts.models import UserProfile, UserPreferences


@login_required
def solo_study_room(request):
    """
    Main solo study room page
    This is where users spend most of their time - immersive study experience
    """
    # Get user's profile and preferences
    profile = request.user.profile
    preferences = request.user.preferences
    
    # Get user's active (incomplete) tasks
    active_tasks = Task.objects.filter(user=request.user, completed=False)
    
    # Get today's stats
    today = timezone.now().date()
    today_minutes = StudySession.objects.filter(
        user=request.user,
        created_at__date=today,
        session_type='focus'
    ).aggregate(Sum('minutes'))['minutes__sum'] or 0
    
    # Pack everything into context
    context = {
        'profile': profile,
        'preferences': preferences,
        'tasks': active_tasks,
        'today_minutes': today_minutes,
    }
    
    return render(request, 'solo/study_room.html', context)


@login_required
@require_POST
def save_study_session(request):
    """
    Save a completed study session
    Called when timer ends (either focus or break)
    """
    try:
        # Get data from request
        data = json.loads(request.body)
        minutes = int(data.get('minutes', 0))
        session_type = data.get('session_type', 'focus')  # focus or break
        task_id = data.get('task_id', None)  # optional
        completed = data.get('completed', True)  # False if stopped early
        
        # Create the session
        session = StudySession.objects.create(
            user=request.user,
            minutes=minutes,
            session_type=session_type,
            completed=completed,
            started_at=timezone.now() - timedelta(minutes=minutes),
            ended_at=timezone.now()
        )
        
        # Link to task if provided
        if task_id:
            try:
                task = Task.objects.get(id=task_id, user=request.user)
                session.task = task
                session.save()
            except Task.DoesNotExist:
                pass
        
        # Update profile stats (only for focus sessions)
        if session_type == 'focus':
            profile = request.user.profile
            leveled_up = profile.update_study_stats(minutes)
            
            # Check for achievements
            new_achievements = check_achievements(request.user)
            
            return JsonResponse({
                'success': True,
                'total_minutes': profile.total_study_minutes,
                'current_streak': profile.study_streak,
                'level': profile.level,
                'xp': profile.total_xp,
                'leveled_up': leveled_up,
                'new_achievements': [
                    {'name': a.achievement.name, 'icon': a.achievement.icon}
                    for a in new_achievements
                ]
            })
        
        return JsonResponse({'success': True})
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@login_required
@require_POST
def update_preferences(request):
    """
    Update user preferences (theme, background, sounds, etc.)
    Called when user changes any setting
    """
    try:
        data = json.loads(request.body)
        preferences = request.user.preferences
        
        # Update any provided fields
        if 'theme' in data:
            preferences.theme = data['theme']
        if 'background' in data:
            preferences.background = data['background']
        if 'ambient_sound' in data:
            preferences.ambient_sound = data['ambient_sound']
        if 'sound_volume' in data:
            preferences.sound_volume = int(data['sound_volume'])
        if 'default_focus_duration' in data:
            preferences.default_focus_duration = int(data['default_focus_duration'])
        if 'default_break_duration' in data:
            preferences.default_break_duration = int(data['default_break_duration'])
        if 'auto_start_breaks' in data:
            preferences.auto_start_breaks = data['auto_start_breaks']
        if 'auto_start_focus' in data:
            preferences.auto_start_focus = data['auto_start_focus']
        if 'show_goals_panel' in data:
            preferences.show_goals_panel = data['show_goals_panel']
        
        preferences.save()
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def check_achievements(user):
    """
    Check if user unlocked any new achievements
    Returns list of newly unlocked achievements
    """
    profile = user.profile
    new_achievements = []
    
    # Get all achievements
    all_achievements = Achievement.objects.all()
    
    for achievement in all_achievements:
        # Check if already unlocked
        if UserAchievement.objects.filter(user=user, achievement=achievement).exists():
            continue
        
        # Check criteria
        unlocked = False
        
        if achievement.criteria_type == 'first_session':
            if StudySession.objects.filter(user=user).exists():
                unlocked = True
        
        elif achievement.criteria_type == 'total_minutes':
            if profile.total_study_minutes >= achievement.criteria_value:
                unlocked = True
        
        elif achievement.criteria_type == 'streak_days':
            if profile.study_streak >= achievement.criteria_value:
                unlocked = True
        
        elif achievement.criteria_type == 'total_sessions':
            session_count = StudySession.objects.filter(user=user, session_type='focus').count()
            if session_count >= achievement.criteria_value:
                unlocked = True
        
        elif achievement.criteria_type == 'level_reached':
            if profile.level >= achievement.criteria_value:
                unlocked = True
        
        elif achievement.criteria_type == 'deep_focus':
            deep_session = StudySession.objects.filter(
                user=user, 
                minutes__gte=achievement.criteria_value
            ).exists()
            if deep_session:
                unlocked = True
        
        # Unlock achievement
        if unlocked:
            user_achievement = UserAchievement.objects.create(
                user=user,
                achievement=achievement
            )
            # Award XP bonus
            profile.add_xp(achievement.xp_reward)
            profile.save()
            new_achievements.append(user_achievement)
    
    return new_achievements
