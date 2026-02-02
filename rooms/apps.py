from django.apps import AppConfig


class RoomsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rooms'
    
    def ready(self):
        """
        Import signals when app is ready
        """
        import rooms.signals
