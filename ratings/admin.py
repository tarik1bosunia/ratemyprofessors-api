# ratings/admin.py

from django.contrib import admin
from .models import (Professor, Course, Rating, Feedback, ProfessorsTag, School,
                     Country, State, SchoolRating, ProfessorRating)

admin.site.register(Professor)
admin.site.register(Course)
admin.site.register(Rating)
admin.site.register(Feedback)
admin.site.register(ProfessorsTag)
admin.site.register(School)
admin.site.register(Country)
admin.site.register(State)
admin.site.register(SchoolRating)
admin.site.register(ProfessorRating)
