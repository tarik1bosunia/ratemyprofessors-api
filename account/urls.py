from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('check-email/', views.CheckEmailExistenceAPIView.as_view(), name='check-email'),
    path('registration/', views.UserRegistrationView.as_view(), name='registration'),
    path('register-professor/', views.ProfessorRegistrationView.as_view(), name='register-professor'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('update-personal-info/', views.UpdateUserPersonalInfoView.as_view(), name='update-personal-info'),
    path('change-password/', views.UserChangePasswordView.as_view(), name='change-password'),
    path('send-password-reset-email/', views.SendPasswordResetEmailView.as_view(), name='send-password-reset-email'),
    path('password-reset-confirm/', views.UserPasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('change-email/', views.UserChangeEmailView.as_view(), name='change-email'),
    path('delete-account/', views.UserDeleteAccountView.as_view(), name='delete-account'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('activate/<str:uid>/<str:token>/', views.ActivateUserView.as_view(), name="activate user email"),
    path('verify/', views.VerifyUserView.as_view(), name="verify user")


]

