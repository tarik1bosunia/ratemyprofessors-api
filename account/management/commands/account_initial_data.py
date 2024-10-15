from django.core.management.base import BaseCommand
from django.core.management import call_command
from ratings.models import Country, State, Department, ProfessorsTag, SchoolRating


class Command(BaseCommand):
    help = "Load initial data  users"

    def handle(self, *args, **kwargs):
        # Load countries
        if not Country.objects.exists():
            print("Loading users data...")
            call_command('loaddata', 'users')
        else:
            print("Users data already exists. Skipping...")
        self.stdout.write(self.style.SUCCESS('Successfully loaded account data'))

