from rest_framework import serializers
from social_auth.utils import Google, register_social_user
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed


class GoogleSignInSerializer(serializers.Serializer):
    access_token = serializers.CharField(min_length=6)

    def validate_access_token(self, access_token):
        google_user_data = Google.validate(access_token)

        try:
            userid = google_user_data['sub']
        except:
            raise serializers.ValidationError('this token is invalid or has expired!')

        if google_user_data['aud'] != settings.GOOGLE_CLIENT_ID:
            raise AuthenticationFailed(detail="could not verify user")

        email = google_user_data['email']
        first_name = google_user_data['given_name']
        last_name = google_user_data['family_name']
        provider = 'google'

        return register_social_user(provider=provider, email=email, first_name=first_name, last_name=last_name)


"""
{
    'iss': 'https://accounts.google.com',
    'azp': '573678907891-8b1nrjprjdqhjgoqkmnseu81jt033ohe.apps.googleusercontent.com',
    'aud': '573678907891-8b1nrjprjdqhjgoqkmnseu81jt033ohe.apps.googleusercontent.com',
    'sub': '105168924894714258917',
    'email': 'bosuniamdtarik005@gmail.com',
    'email_verified': True, 
    'nbf': 1722402678, 
    'name': 'MD Tarik Bosunia',
    'picture': 'https://lh3.googleusercontent.com/a/ACg8ocIYXBvT5IQ6peB5uix49zrisSsbSeQl9vXat_M8w4X-_jJKvIHJ=s96-c',
    'given_name': 'MD Tarik',
    'family_name': 'Bosunia',
    'iat': 1722402978,
    'exp': 1722406578,
    'jti': 'de1918ebb685a01c9f3d8001980152f70830bae7'
}

"""
