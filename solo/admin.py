# solo/admin.py
"""
Admin interface for Solo Study Room
Note: Task, Achievement, and UserAchievement are registered in tracker/admin.py
"""
from django.contrib import admin
from accounts.models import UserPreferences


@admin.register(UserPreferences)
class UserPreferencesAdmin(admin.ModelAdmin):
    list_display = ('user', 'theme', 'background', 'ambient_sound', 'default_focus_duration')
    list_filter = ('theme', 'background', 'ambient_sound')
    search_fields = ('user__username',)

