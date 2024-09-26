from ratings.models import Professor
from .serializers import EmailCheckSerializer, UserUpdatePersonalInfoSerializer, UserChangeEmailSerializer, \
    UserDeleteAccountSerializer
from django.contrib.auth import get_user_model

from django.contrib.auth import authenticate

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from account.serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, \
    UserChangePasswordSerializer, SendPasswordResetEmailSerializer, UserPasswordResetConfirmSerializer
from account.renderers import UserRenderer

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, smart_str, DjangoUnicodeDecodeError
from account.utils import Util

from django.contrib.auth.tokens import default_token_generator

User = get_user_model()


# Generate Token Manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class CheckEmailExistenceAPIView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, *args, **kwargs):
        serializer = EmailCheckSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']

        if User.objects.filter(email=email).exists():
            return Response({'exists': True, 'message': 'An account with this email already exists.'},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'exists': False, 'message': 'Email does not exist.'}, status=status.HTTP_200_OK)


class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        print(request.data)
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()

            token = get_tokens_for_user(user)

            # Send registration email
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token_activate_email = default_token_generator.make_token(user)

            reset_link = f'http://127.0.0.1:8000/api/user/activate/{uid}/{token_activate_email}/'
            body = f'Click the following link to verify your email in ratemyprofessors: {reset_link}'
            data = {
                'subject': 'verify your email',
                'body': body,
                'to_email': user.email
            }

            Util.send_email(data)
            return Response({'token': token, "message": "Registration Successful"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfessorRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        print(request.data)
        professor_id = request.data.get('id')
        print(professor_id)
        try:
            # Retrieve the Professor object by the given ID
            professor = Professor.objects.get(id=professor_id)
            print(professor)
        except Professor.DoesNotExist:
            return Response({"error": "Professor not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()

            # Associate the user with the existing Professor object
            try:
                print(f"Professor before association: {professor}")
                professor.user = user
                professor.save()
                print(f"Professor after association: {professor}")
            except Exception as e:
                print(f"Error while saving professor: {e}")
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            token = get_tokens_for_user(user)

            # Send registration email
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token_activate_email = default_token_generator.make_token(user)

            reset_link = f'http://127.0.0.1:8000/api/user/activate/{uid}/{token_activate_email}/'
            body = f'Click the following link to verify your email in ratemyprofessors: {reset_link}'
            data = {
                'subject': 'verify your email',
                'body': body,
                'to_email': user.email
            }

            Util.send_email(data)
            return Response({'token': token, "message": "Registration Successful"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ProfessorRegistrationView(APIView):
#     renderer_classes = [UserRenderer]  # Assuming UserRenderer is defined
#
#     def post(self, request, format=None):
#         print(request.data)
#         professor_id = request.data.get('id')
#
#         try:
#             # Retrieve the Professor object by the given ID
#             professor = Professor.objects.get(id=professor_id)
#         except Professor.DoesNotExist:
#             return Response({"error": "Professor not found"}, status=status.HTTP_404_NOT_FOUND)
#
#         # Register the user
#         serializer = UserRegistrationSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             user = serializer.save()
#
#             # Associate the user with the existing Professor object
#             professor.user = user
#             professor.save()
#
#             # Generate token for the user
#             token = get_tokens_for_user(user)
#
#             # Send registration email
#             uid = urlsafe_base64_encode(force_bytes(user.id))
#             token_activate_email = default_token_generator.make_token(user)
#             reset_link = f'http://127.0.0.1:8000/api/user/activate/{uid}/{token_activate_email}/'
#             body = f'Click the following link to verify your email in ratemyprofessors: {reset_link}'
#             email_data = {
#                 'subject': 'Verify your email',
#                 'body': body,
#                 'to_email': user.email,
#             }
#
#             Util.send_email(email_data)
#
#             return Response({'token': token, "message": "Registration Successful"}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'token': token, 'message': 'Login Success'}, status=status.HTTP_200_OK)
        else:
            return Response({'errors': {'non_field_errors': ['Email or Password is not Valid']}},
                            status=status.HTTP_404_NOT_FOUND)


class UpdateUserPersonalInfoView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = UserUpdatePersonalInfoSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # Pass the user instance directly to the serializer
        serializer = UserProfileSerializer(request.user, context={'user': request.user})
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        email = request.user.email
        old_password = request.data.get('old_password')
        user = authenticate(email=email, password=old_password)
        if user is not None:
            serializer = UserChangePasswordSerializer(data=request.data, context={'user': request.user})
            serializer.is_valid(raise_exception=True)
            return Response({'msg': 'Password Changed Successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'errors': {'old_password': ['Invalid Credentials']}},
                            status=status.HTTP_404_NOT_FOUND)


class UserChangeEmailView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = UserChangeEmailSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Email successfully updated'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)


class UserPasswordResetConfirmView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserPasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password Reset Successfully'}, status=status.HTTP_200_OK)


class UserDeleteAccountView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        print(request.data)
        serializer = UserDeleteAccountSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            user.delete()
            return Response({'message': 'Account deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        return Response({'message': 'Logout successful'}, status=status.HTTP_204_NO_CONTENT)


class ActivateUserView(APIView):
    def get(self, request, uid, token):
        try:
            # Decode the uid
            uid = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=uid)

            # Check if the token is valid
            if default_token_generator.check_token(user, token):
                user.is_email_verified = True  # Mark email as verified
                user.save()
                return Response({'message': 'Account activated successfully!'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid token or token has expired.'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'Invalid user.'}, status=status.HTTP_400_BAD_REQUEST)


class VerifyUserView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        token = get_tokens_for_user(request.user)
        return Response({'token': token, "message": "User is verified"}, status=status.HTTP_200_OK)