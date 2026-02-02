# solo/apps.py
from django.apps import AppConfig


class SoloConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'solo'
    verbose_name = 'Solo Study Room'
