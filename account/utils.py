from django.contrib.auth import authenticate
from django.core.mail import EmailMessage
import os

from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from account.models import User


class Util:

    @staticmethod
    def send_email(data):

        print(data['body'])
        email = EmailMessage(
            subject=data['subject'],
            body=data['body'],
            from_email=os.environ.get('EMAIL_FROM'),
            to=[data['to_email']]
        )
        email.send()

    @staticmethod
    def get_tokens_for_user(user):
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    @staticmethod
    def login_user(email, password):
        user = authenticate(email=email, password=password)

        if user is not None:
            token = Util.get_tokens_for_user(user)
            return Response({'token': token, 'message': 'Login Success'}, status=status.HTTP_200_OK)
        else:
            print('Email or Password is not Valid')
            return Response({'errors': {'non_field_errors': ['Email or Password is not Valid']}},
                            status=status.HTTP_404_NOT_FOUND)