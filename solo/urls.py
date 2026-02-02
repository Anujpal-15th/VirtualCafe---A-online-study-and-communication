# solo/urls.py
"""
URL patterns for Solo Study Room
"""
from django.urls import path
from . import views, task_views

app_name = 'solo'

urlpatterns = [
    # Main study room
    path('', views.solo_study_room, name='study_room'),
    
    # Session management
    path('save-session/', views.save_study_session, name='save_session'),
    path('update-preferences/', views.update_preferences, name='update_preferences'),
    
    # Task API endpoints
    path('tasks/', task_views.get_tasks, name='get_tasks'),
    path('tasks/create/', task_views.create_task, name='create_task'),
    path('tasks/<int:task_id>/update/', task_views.update_task, name='update_task'),
    path('tasks/<int:task_id>/toggle/', task_views.toggle_task, name='toggle_task'),
    path('tasks/<int:task_id>/delete/', task_views.delete_task, name='delete_task'),
]
