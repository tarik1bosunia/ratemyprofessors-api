# ratings/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.search import SearchVector
from .models import School, Professor
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=School)
def update_school_search_vector(sender, instance, **kwargs):
    search_vector = (
        SearchVector('name_of_school', weight='A') +
        SearchVector('location', weight='B') +
        SearchVector('country__name', weight='C') +
        SearchVector('state__name', weight='D')
    )
    instance.search_vector = search_vector
    instance.save()

@receiver(post_save, sender=Professor)
def update_professor_search_vector(sender, instance, **kwargs):
    search_vector = (
        SearchVector('first_name', weight='A') +
        SearchVector('last_name', weight='A') +
        SearchVector('middle_name', weight='B') +
        SearchVector('department__name', weight='C') +
        SearchVector('name_of_school', weight='D')
    )
    logger.debug(f"Search vector updated for professor: {instance.id}")
    instance.search_vector = search_vector
    instance.save()


# python manage.py update_search_vector