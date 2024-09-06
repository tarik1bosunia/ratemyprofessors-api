# ratings/admin.py

from django.contrib import admin
from .models import (
    Department, Professor, Course, Rating, Feedback,
    ProfessorsTag, Country, State, School, SchoolRating,
    ProfessorRating
)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'name_of_school', 'department')
    search_fields = ('first_name', 'last_name', 'name_of_school', 'department__name')
    list_filter = ('department',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'professor')
    search_fields = ('name', 'code', 'professor__first_name', 'professor__last_name')
    list_filter = ('professor',)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('course', 'reputation', 'comment')
    search_fields = ('course__name', 'comment')
    list_filter = ('reputation',)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('professor', 'would_take_again', 'level_of_difficulty')
    search_fields = ('professor__first_name', 'professor__last_name')
    list_filter = ('would_take_again', 'level_of_difficulty')


@admin.register(ProfessorsTag)
class ProfessorsTagAdmin(admin.ModelAdmin):
    list_display = ('tag',)
    search_fields = ('tag',)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    search_fields = ('name', 'country__name')
    list_filter = ('country',)


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name_of_school', 'location', 'country', 'state')
    search_fields = ('name_of_school', 'location', 'country__name', 'state__name')
    list_filter = ('country', 'state')


@admin.register(SchoolRating)
class SchoolRatingAdmin(admin.ModelAdmin):
    list_display = ('school', 'user', 'reputation', 'created_at')
    search_fields = ('school__name_of_school', 'user__username', 'comment')
    list_filter = ('reputation', 'created_at')


@admin.register(ProfessorRating)
class ProfessorRatingAdmin(admin.ModelAdmin):
    list_display = ('professor', 'course_code', 'rating', 'difficulty', 'is_online_course', 'is_take_professor_again')
    search_fields = ('professor__first_name', 'professor__last_name', 'course_code', 'comment')
    list_filter = ('rating', 'difficulty', 'is_online_course', 'is_take_professor_again')


# from django.contrib import admin
# from .models import (Professor, Course, Rating, Feedback, ProfessorsTag, School,
#                      Country, State, SchoolRating, ProfessorRating)
#
#
# admin.site.register(Professor)
# admin.site.register(Course)
# admin.site.register(Rating)
# admin.site.register(Feedback)
# admin.site.register(ProfessorsTag)
# admin.site.register(School)
# admin.site.register(Country)
# admin.site.register(State)
# admin.site.register(SchoolRating)
# admin.site.register(ProfessorRating)
