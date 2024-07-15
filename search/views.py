from rest_framework import generics
from rest_framework.filters import SearchFilter

from ratings.models import Professor, School
from ratings.serializers import ProfessorSerializer, SchoolSerializer


class ProfessorSearchAPIView(generics.ListAPIView):
    serializer_class = ProfessorSerializer
    queryset = Professor.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['first_name', 'last_name', 'middle_name', 'name_of_school', 'department__name']


class SchoolSearchAPIView(generics.ListAPIView):
    serializer_class = SchoolSerializer
    queryset = School.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['name_of_school', 'location', 'country__name', 'state__name']