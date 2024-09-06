from django.urls import path
from . import views


urlpatterns = [
    path('google/', views.GoogleSignInView.as_view(), name='google'),
]
