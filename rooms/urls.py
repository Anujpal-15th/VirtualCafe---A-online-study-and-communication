"""
Rooms app URL patterns.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_view, name='landing'),
    path('dashboard/', views.home_view, name='home'),
    path('rooms/create/', views.create_room_view, name='create_room'),
    path('rooms/<str:room_code>/', views.room_detail_view, name='room_detail'),
]
