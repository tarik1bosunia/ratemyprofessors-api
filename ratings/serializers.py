# ratings/serializers.py
from django.db.models import Avg
from rest_framework import serializers
from .models import Professor, Course, Rating, Feedback, ProfessorsTag, School, State, Country, Department, \
    SchoolRating, ProfessorRating


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'course', 'rating', 'comment']


class CourseSerializer(serializers.ModelSerializer):
    ratings = RatingSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'code', 'professor', 'ratings']


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'professor', 'would_take_again', 'level_of_difficulty']


class ProfessorsTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessorsTag
        fields = ['id', 'tag']


class ProfessorSerializer(serializers.ModelSerializer):
    # courses = CourseSerializer(many=True, read_only=True)
    # feedback = FeedbackSerializer(many=True, read_only=True)
    # tags = TagSerializer(many=True, read_only=True)
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())

    class Meta:
        model = Professor
        fields = ['id', 'name_of_school', 'first_name', 'middle_name', 'last_name', 'department', 'directory_listing_of_professor']


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ('id', 'name')


class CountrySerializer(serializers.ModelSerializer):
    states = StateSerializer(many=True, read_only=True)

    class Meta:
        model = Country
        fields = ('id', 'name', 'states')


class SchoolSerializer(serializers.ModelSerializer):
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all())
    state = serializers.PrimaryKeyRelatedField(queryset=State.objects.all(), allow_null=True, required=False)

    class Meta:
        model = School
        fields = ['id', 'name_of_school', 'school_website', 'location', 'state', 'country', 'terms_privacy']


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name']


class SchoolRatingSerializer(serializers.ModelSerializer):
    school = serializers.PrimaryKeyRelatedField(queryset=School.objects.all())
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = SchoolRating
        fields = '__all__'  # Include all fields of the SchoolRating model


class ProfessorRatingSerializer(serializers.ModelSerializer):
    professor = serializers.PrimaryKeyRelatedField(queryset=Professor.objects.all())
    tags = serializers.SlugRelatedField(many=True, queryset=ProfessorsTag.objects.all(), slug_field='tag')

    class Meta:
        model = ProfessorRating
        fields = [
            'professor', 'course_code', 'is_online_course', 'rating', 'difficulty',
            'is_take_professor_again', 'was_class_taken_for_credit',
            'was_use_textbook', 'was_attendance_mandatory', 'grade',
            'tags', 'comment', 'created_at'
        ]


class SimilarProfessorSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Professor
        fields = ['id', 'first_name', 'last_name', 'average_rating']

    def get_average_rating(self, obj):
        ratings = ProfessorRating.objects.filter(professor=obj)
        if ratings.exists():
            return ratings.aggregate(Avg('rating'))['rating__avg']
        return None