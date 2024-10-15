from django.core.management.base import BaseCommand
from django.core.management import call_command
from ratings.models import Country, State, Department, ProfessorsTag, SchoolRating, School


class Command(BaseCommand):
    help = "Load initial data for countries, states, departments, professor tags, School, and school ratings."

    def handle(self, *args, **kwargs):
        # Load countries
        if not Country.objects.exists():
            print("Loading countries data...")
            call_command('loaddata', 'countries')
        else:
            print("Countries data already exists. Skipping...")

        # Load states
        if not State.objects.exists():
            print("Loading states data...")
            call_command('loaddata', 'states')
        else:
            print("States data already exists. Skipping...")

        # Load departments
        if not Department.objects.exists():
            print("Loading departments data...")
            call_command('loaddata', 'departments')
        else:
            print("Departments data already exists. Skipping...")

        # Load professor tags
        if not ProfessorsTag.objects.exists():
            print("Loading ProfessorsTags data...")
            call_command('loaddata', 'professors_tags')
        else:
            print("ProfessorsTags data already exists. Skipping...")

        # Load school ratings
        if not School.objects.exists():
            print("Loading School data...")
            call_command('loaddata', 'schools.json')
        else:
            print("School data already exists. Skipping...")

        # Load school ratings
        if not SchoolRating.objects.exists():
            print("Loading SchoolRatings data...")
            call_command('loaddata', 'school_ratings.json')
        else:
            print("SchoolRatings data already exists. Skipping...")

        self.stdout.write(self.style.SUCCESS('Successfully loaded ratings data'))