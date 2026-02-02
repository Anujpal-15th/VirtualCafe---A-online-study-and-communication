"""
Management command to populate achievements
Run with: python manage.py create_achievements
"""
from django.core.management.base import BaseCommand
from tracker.models import Achievement


class Command(BaseCommand):
    help = 'Create initial achievements for gamification'

    def handle(self, *args, **options):
        achievements_data = [
            # First session achievements
            {
                'name': 'Getting Started',
                'description': 'Complete your first focus session',
                'icon': '🎯',
                'criteria_type': 'first_session',
                'criteria_value': 1,
                'xp_reward': 50
            },
            
            # Total minutes achievements
            {
                'name': 'Hour Master',
                'description': 'Study for 60 total minutes',
                'icon': '⏰',
                'criteria_type': 'total_minutes',
                'criteria_value': 60,
                'xp_reward': 100
            },
            {
                'name': 'Half Day Scholar',
                'description': 'Study for 6 hours total',
                'icon': '📚',
                'criteria_type': 'total_minutes',
                'criteria_value': 360,
                'xp_reward': 200
            },
            {
                'name': 'Study Marathon',
                'description': 'Study for 24 hours total',
                'icon': '🏃',
                'criteria_type': 'total_minutes',
                'criteria_value': 1440,
                'xp_reward': 500
            },
            
            # Streak achievements
            {
                'name': 'Consistent Learner',
                'description': 'Study for 3 days in a row',
                'icon': '🔥',
                'criteria_type': 'streak_days',
                'criteria_value': 3,
                'xp_reward': 150
            },
            {
                'name': 'Week Warrior',
                'description': 'Study for 7 days in a row',
                'icon': '💪',
                'criteria_type': 'streak_days',
                'criteria_value': 7,
                'xp_reward': 300
            },
            {
                'name': 'Month Champion',
                'description': 'Study for 30 days in a row',
                'icon': '👑',
                'criteria_type': 'streak_days',
                'criteria_value': 30,
                'xp_reward': 1000
            },
            
            # Total sessions achievements
            {
                'name': 'Session Starter',
                'description': 'Complete 10 focus sessions',
                'icon': '✨',
                'criteria_type': 'total_sessions',
                'criteria_value': 10,
                'xp_reward': 100
            },
            {
                'name': 'Dedicated Student',
                'description': 'Complete 50 focus sessions',
                'icon': '🌟',
                'criteria_type': 'total_sessions',
                'criteria_value': 50,
                'xp_reward': 300
            },
            {
                'name': 'Study Veteran',
                'description': 'Complete 100 focus sessions',
                'icon': '💎',
                'criteria_type': 'total_sessions',
                'criteria_value': 100,
                'xp_reward': 750
            },
            
            # Level achievements
            {
                'name': 'Leveling Up',
                'description': 'Reach level 5',
                'icon': '📈',
                'criteria_type': 'level_reached',
                'criteria_value': 5,
                'xp_reward': 200
            },
            {
                'name': 'Rising Star',
                'description': 'Reach level 10',
                'icon': '⭐',
                'criteria_type': 'level_reached',
                'criteria_value': 10,
                'xp_reward': 500
            },
            
            # Deep focus achievements
            {
                'name': 'Deep Focus',
                'description': 'Complete a 90-minute session',
                'icon': '🧘',
                'criteria_type': 'deep_focus',
                'criteria_value': 90,
                'xp_reward': 200
            },
            {
                'name': 'Ultra Focus',
                'description': 'Complete a 2-hour session',
                'icon': '🎓',
                'criteria_type': 'deep_focus',
                'criteria_value': 120,
                'xp_reward': 300
            },
        ]
        
        created_count = 0
        for achievement_data in achievements_data:
            achievement, created = Achievement.objects.get_or_create(
                name=achievement_data['name'],
                defaults=achievement_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created: {achievement.icon} {achievement.name}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\nCreated {created_count} new achievements!')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Total achievements in database: {Achievement.objects.count()}')
        )
