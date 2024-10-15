# ratings/views.py

from rest_framework import viewsets, status
from rest_framework.exceptions import NotFound
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView

from .models import Professor, Course, Rating, Feedback, ProfessorsTag, School, State, Country, Department, \
    SchoolRating, ProfessorRating
from .serializers import ProfessorSerializer, CourseSerializer, RatingSerializer, FeedbackSerializer, \
    ProfessorsTagSerializer, \
    SchoolSerializer, CountrySerializer, StateSerializer, DepartmentSerializer, SchoolRatingSerializer, \
    ProfessorRatingSerializer, SimilarProfessorSerializer

from rest_framework import generics, pagination
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.decorators import action

from account.renderers import UserRenderer

from django.db.models import Q, Avg, Count

from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector, TrigramSimilarity, TrigramDistance, \
    SearchHeadline


class CustomPagination(pagination.PageNumberPagination):
    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProfessorListAPIView(generics.ListAPIView):
    renderer_classes = [UserRenderer]

    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    permission_classes = []  # Allow everyone to view


class ProfessorCreateAPIView(generics.CreateAPIView):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        print("Request Data:", request.data)
        print("Request Headers:", request.headers)
        if 'department' not in request.data:
            print("Department is missing from request data")
        return super().create(request, *args, **kwargs)

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProfessorsTag.objects.all()
    serializer_class = ProfessorsTagSerializer


class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class StateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer

    @action(detail=False, methods=['get'])
    def by_country(self, request, pk=None):
        country_id = request.query_params.get('country_id')
        if country_id:
            states = self.queryset.filter(country_id=country_id)
            serializer = self.get_serializer(states, many=True)
            return Response(serializer.data)
        return Response([])


class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [AllowAny]  # Default to allow any for viewing actions
        return super().get_permissions()

    def update(self, request, *args, **kwargs):
        return Response({'detail': 'Method "PUT" not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        return Response({'detail': 'Method "PATCH" not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return Response({'detail': 'Method "DELETE" not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class SchoolRatingAPIView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get(self, request, school_id, rating_id=None):
        if rating_id:
            rating = get_object_or_404(SchoolRating, id=rating_id, school_id=school_id)
            serializer = SchoolRatingSerializer(rating)
            return Response(serializer.data)
        else:
            ratings = SchoolRating.objects.filter(school_id=school_id)
            serializer = SchoolRatingSerializer(ratings, many=True)
            return Response(serializer.data)

    def post(self, request, school_id):
        data = request.data
        data['school'] = school_id  # Assign the school ID to the rating data

        serializer = SchoolRatingSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Save the rating with the current user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RateProfessorView(generics.CreateAPIView):
    queryset = ProfessorRating.objects.all()
    serializer_class = ProfessorRatingSerializer

    def create(self, request, *args, **kwargs):
        # Extract the professor_id from the URL
        professor_id = kwargs.get('professor_id')

        # Ensure the professor exists
        try:
            professor = Professor.objects.get(id=professor_id)
        except Professor.DoesNotExist:
            return Response({"error": "Professor not found"}, status=status.HTTP_404_NOT_FOUND)


        # Extract and validate request data
        data = request.data.copy()
        print(data)
        data['professor'] = professor_id

        # Validate tags (ensure they are valid tag IDs)
        tag_ids = data.get('tags', [])
        if not all(isinstance(tag_id, int) for tag_id in tag_ids):
            return Response({"error": "Tags must be a list of integers"}, status=status.HTTP_400_BAD_REQUEST)

        # Validate tags (ensure they are valid tag IDs)
        tag_ids = data.get('tags', [])
        if not all(isinstance(tag_id, int) for tag_id in tag_ids):
            return Response({"error": "Tags must be a list of integers"}, status=status.HTTP_400_BAD_REQUEST)

        # Validate and create the ProfessorRating object
        serializer = self.get_serializer(data=data)
        # serializer.is_valid(raise_exception=True)
        # self.perform_create(serializer)

        if serializer.is_valid(raise_exception=False):
            self.perform_create(serializer)
        else:
            print(serializer.errors)  # Log the errors for debugging
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Return the response with the created object data
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# get a professor ratings by his/her id
class ProfessorRatingsView(generics.ListAPIView):
    serializer_class = ProfessorRatingSerializer

    def get_queryset(self):
        # Extract the professor_id from the URL
        professor_id = self.kwargs.get('professor_id')

        # Ensure the professor exists
        try:
            professor = Professor.objects.get(id=professor_id)
        except Professor.DoesNotExist:
            return Response({"error": "Professor not found"}, status=status.HTTP_404_NOT_FOUND)

        # Return all ratings for the professor
        return ProfessorRating.objects.filter(professor=professor)

    def get(self, request, *args, **kwargs):
        # Get the queryset using the get_queryset method
        queryset = self.get_queryset()

        # Count how many ratings exist
        total_ratings_count = queryset.count()

        # Count how many times is_take_professor_again is True
        take_again_count = queryset.filter(is_take_professor_again=True).count()

        # Calculate the average level of difficulty
        avg_difficulty = queryset.aggregate(Avg('difficulty'))['difficulty__avg']

        # Get the top 5 most common tags
        top_tags = ProfessorRating.objects.filter(professor__id=self.kwargs.get('professor_id')).values('tags__tag')\
            .annotate(tag_count=Count('tags'))\
            .order_by('-tag_count')[:5]

        # Count how many times each rating appears
        rating_counts = queryset.values('rating').annotate(count=Count('rating')).order_by('rating')

        # Calculate the percentage of take_again_count
        take_again_percentage = int((take_again_count / total_ratings_count * 100) if total_ratings_count > 0 else 0)

        # Serialize the professor
        professor = Professor.objects.get(id=self.kwargs.get('professor_id'))
        professor_serializer = ProfessorSerializer(professor)

        # Serialize the data
        serializer = self.get_serializer(queryset, many=True)

        # Return the serialized data along with the count
        return Response({
            "professor": professor_serializer.data,
            "ratings": serializer.data,
            "total_ratings_count": total_ratings_count,
            "take_again_count": take_again_count,
            "avg_difficulty": f"{avg_difficulty:.2f}" if avg_difficulty is not None else "N/A",
            "top_tags": list(top_tags),
            "rating_counts": list(rating_counts),
            "take_again_percentage": take_again_percentage,

        })


class SimilarProfessorsView(generics.ListAPIView):
    serializer_class = SimilarProfessorSerializer

    def get_queryset(self):
        professor_id = self.kwargs.get('professor_id')
        professor = get_object_or_404(Professor, id=professor_id)
        # Get professors in the same department, excluding the current professor
        return Professor.objects.filter(department=professor.department).exclude(id=professor_id)