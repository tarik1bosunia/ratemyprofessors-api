# ratings/urls.py

from django.urls import path
from .views import ProfessorSearchAPIView, SchoolSearchAPIView

urlpatterns = [

    path('schools/', SchoolSearchAPIView.as_view(), name='school-search'),
    path('professors/', ProfessorSearchAPIView.as_view(), name='professor-search'),
]
