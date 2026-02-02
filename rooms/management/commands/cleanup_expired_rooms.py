"""
Management command to clean up expired rooms.
Run this periodically (e.g., via cron job) to remove empty rooms that have expired.
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from rooms.models import Room


class Command(BaseCommand):
    help = 'Removes rooms that have been empty for more than 15 minutes'

    def handle(self, *args, **options):
        # Find expired rooms
        expired_rooms = Room.objects.filter(
            expires_at__lte=timezone.now()
        )
        
        count = expired_rooms.count()
        
        if count > 0:
            # Get room names for logging
            room_names = list(expired_rooms.values_list('name', flat=True))
            
            # Delete expired rooms
            expired_rooms.delete()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully deleted {count} expired room(s): {", ".join(room_names)}'
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('No expired rooms found.')
            )
        
        # Update expiration for empty rooms that don't have expiration set
        empty_rooms_without_expiration = Room.objects.filter(
            expires_at__isnull=True
        )
        
        updated_count = 0
        for room in empty_rooms_without_expiration:
            if room.is_empty():
                room.update_activity()
                updated_count += 1
        
        if updated_count > 0:
            self.stdout.write(
                self.style.WARNING(
                    f'Set expiration time for {updated_count} empty room(s).'
                )
            )
