# ratings/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (ProfessorListAPIView, ProfessorCreateAPIView, CourseViewSet, RatingViewSet, FeedbackViewSet,
                    TagViewSet, CountryViewSet, StateViewSet, SchoolViewSet, DepartmentViewSet, SchoolRatingAPIView,
                    RateProfessorView, ProfessorRatingsView, SimilarProfessorsView, GetAverageRatingSchool,
                    GetProfessorRatingsView, CourseCodesByProfessorView)

router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'ratings', RatingViewSet)
router.register(r'feedback', FeedbackViewSet)
router.register(r'professors_tags', TagViewSet)
router.register(r'countries', CountryViewSet)
router.register(r'states', StateViewSet)
router.register(r'schools', SchoolViewSet)
router.register(r'departments', DepartmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('states/by_country/', StateViewSet.as_view({'get': 'by_country'}), name='states-by-country'),
    path('professors/', ProfessorListAPIView.as_view(), name='professor-list'),
    path('professors/create/', ProfessorCreateAPIView.as_view(), name='professor-create'),
    path('school-rating/<int:school_id>/', SchoolRatingAPIView.as_view(), name='school-rating'),
    path('school-rating/<int:school_id>/<int:rating_id>/', SchoolRatingAPIView.as_view()),
    path('average-ratings-school/<int:school_id>/', GetAverageRatingSchool.as_view(), name='average-ratings-school'),
    path('professor-rating/<int:professor_id>/', RateProfessorView.as_view(), name='rate-professor'),
    path('professors/<int:professor_id>/', ProfessorRatingsView.as_view(), name='professor-details'),
    path('professors/<int:professor_id>/ratings/', GetProfessorRatingsView.as_view(), name='professor-ratings'),
    path('professors/<int:professor_id>/course_codes/', CourseCodesByProfessorView.as_view(), name='professor-course'
                                                                                                   '-codes'),
    path('professors/<int:professor_id>/similar/', SimilarProfessorsView.as_view(), name='similar-professors'),

]
