from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework import status
from rest_framework.response import Response

from account.models import User
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from account.utils import Util


class Google():
    @staticmethod
    def validate(access_token):
        try:
            id_info = id_token.verify_oauth2_token(access_token, requests.Request())
            if 'accounts.google.com' in id_info['iss']:
                return id_info

        except Exception as e:
            return "token is invalid or has expired!"


def login_social_user(email, password):
    user = authenticate(email=email, password=password)

    if user is not None:
        token = Util.get_tokens_for_user(user)
        print('token: ', token)
        return {'token': token, 'message': 'Login Success'}

    else:
        return {'errors': {'non_field_errors': ['Email or Password is not Valid']}}


def register_social_user(provider, email, first_name, last_name):
    user = User.objects.filter(email=email)
    if user.exists():
        if provider == user[0].auth_provider:
            return login_social_user(email, password=settings.SOCIAL_AUTH_PASSWORD)
        else:
            raise AuthenticationFailed(
                detail=f'Please continue login with{user[0].auth_provider}'
            )

    else:
        new_registered_user = User.objects.create_user(
            email=email, first_name=first_name,
            last_name=last_name,
            password=settings.SOCIAL_AUTH_PASSWORD
        )
        new_registered_user.auth_provider = provider
        new_registered_user.is_active = True
        new_registered_user.save()

        return login_social_user(new_registered_user.email, password=settings.SOCIAL_AUTH_PASSWORD)