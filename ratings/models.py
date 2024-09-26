# ratings/models.py

from django.db import models
from account.models import User
from django.contrib.postgres.fields import ArrayField

# search
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex


class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Professor(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, related_name='professor', null=True, blank=True)
    name_of_school = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, related_name='professors', on_delete=models.CASCADE)
    directory_listing_of_professor = models.TextField(blank=True, null=True)
    terms_privacy = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"




class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    professor = models.ForeignKey(Professor, related_name='courses', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Rating(models.Model):
    course = models.ForeignKey(Course, related_name='ratings', on_delete=models.CASCADE)
    reputation = models.IntegerField()
    location = models.IntegerField()
    opportunities = models.IntegerField()
    facilities = models.IntegerField()
    internet = models.IntegerField()
    food = models.IntegerField()
    clubs = models.IntegerField()
    social = models.IntegerField()
    happiness = models.IntegerField()
    comment = models.TextField()

    def __str__(self):
        return f"{self.course.name} - {self.reputation}"


class Feedback(models.Model):
    professor = models.ForeignKey(Professor, related_name='feedback', on_delete=models.CASCADE)
    would_take_again = models.BooleanField()
    level_of_difficulty = models.FloatField()


class ProfessorsTag(models.Model):
    tag = models.CharField(max_length=50)


class Country(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=2, unique=True)  # ISO 3166-1 alpha-2 code

    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, related_name='states', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class School(models.Model):
    name_of_school = models.CharField(max_length=255)
    school_website = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    country = models.ForeignKey(Country, related_name='schools', on_delete=models.CASCADE, null=True, blank=True)
    state = models.ForeignKey(State, related_name='schools', on_delete=models.CASCADE, null=True, blank=True)
    terms_privacy = models.BooleanField(default=False)

    def __str__(self):
        return self.name_of_school


class SchoolRating(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='school_ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reputation = models.IntegerField()
    facilities = models.IntegerField()
    internet = models.IntegerField()
    food = models.IntegerField()
    clubs = models.IntegerField()
    social = models.IntegerField()
    happiness = models.IntegerField()
    safety = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.school.name_of_school}'


class ProfessorRating(models.Model):
    RATING_CHOICES = [
        (1, 'Awful'),
        (2, 'Ok'),
        (3, 'Good'),
        (4, 'Great'),
        (5, 'Awesome'),
    ]
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    course_code = models.CharField(max_length=100)
    is_online_course = models.BooleanField(default=False)
    rating = models.IntegerField(choices=RATING_CHOICES)
    difficulty = models.IntegerField()
    is_take_professor_again = models.BooleanField()
    was_class_taken_for_credit = models.BooleanField(null=True, blank=True)
    was_use_textbook = models.BooleanField(null=True, blank=True)
    was_attendance_mandatory = models.BooleanField(null=True)
    grade = models.CharField(max_length=20, null=True, blank=True)
    tags = models.ManyToManyField(ProfessorsTag, blank=True)
    comment = models.TextField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.professor} - {self.course_code} - {self.rating}"
