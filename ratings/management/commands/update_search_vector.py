# ratings/management/commands/update_search_vector.py

from django.core.management.base import BaseCommand
from django.contrib.postgres.search import SearchVector
from ratings.models import School, Professor


class Command(BaseCommand):
    help = 'Update search vector for existing School and Professor data'

    def handle(self, *args, **kwargs):
        for school in School.objects.all():
            search_vector = (
                    SearchVector('name_of_school', weight='A') +
                    SearchVector('location', weight='B') +
                    SearchVector('country__name', weight='C') +
                    SearchVector('state__name', weight='D')
            )
            school.search_vector = search_vector
            school.save()

        for professor in Professor.objects.all():
            search_vector = (
                    SearchVector('first_name', weight='A') +
                    SearchVector('last_name', weight='A') +
                    SearchVector('middle_name', weight='B') +
                    SearchVector('department__name', weight='C') +
                    SearchVector('name_of_school', weight='D')
            )
            professor.search_vector = search_vector
            professor.save()

        self.stdout.write(self.style.SUCCESS('Successfully updated search vectors.'))
