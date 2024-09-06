# from django.conf import settings
# from django.urls import reverse_lazy
# from .get_google_credentials import google_sdk_login_get_credentials
# import google_auth_oauthlib.flow
#
#
# class GoogleSdkLoginFlowService:
#     API_URI = reverse_lazy("api:google-oauth2:login-sdk:callback-sdk")
#
#     # Two options are available: 'web', 'installed'
#     GOOGLE_CLIENT_TYPE = "web"
#
#     GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
#     GOOGLE_ACCESS_TOKEN_OBTAIN_URL = "https://oauth2.googleapis.com/token"
#     GOOGLE_USER_INFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"
#
#     # Add auth_provider_x509_cert_url if you want verification on JWTS such as ID tokens
#     GOOGLE_AUTH_PROVIDER_CERT_URL = ""
#
#     SCOPES = [
#         "https://www.googleapis.com/auth/userinfo.email",
#         "https://www.googleapis.com/auth/userinfo.profile",
#         "openid",
#     ]
#
#     def __init__(self):
#         self._credentials = google_sdk_login_get_credentials()
#
#     def _get_redirect_uri(self):
#         domain = settings.BASE_BACKEND_URL
#         api_uri = self.API_URI
#         redirect_uri = f"{domain}{api_uri}"
#         return redirect_uri
#
#     def _generate_client_config(self):
#         # This follows the structure of the official "client_secret.json" file
#         client_config = {
#             self.GOOGLE_CLIENT_TYPE: {
#                 "client_id": self._credentials.client_id,
#                 "project_id": self._credentials.project_id,
#                 "auth_uri": self.GOOGLE_AUTH_URL,
#                 "token_uri": self.GOOGLE_ACCESS_TOKEN_OBTAIN_URL,
#                 "auth_provider_x509_cert_url": self.GOOGLE_AUTH_PROVIDER_CERT_URL,
#                 "client_secret": self._credentials.client_secret,
#                 "redirect_uris": [self._get_redirect_uri()],
#                 # If you are dealing with single page applications,
#                 # you'll need to set this both in Google API console
#                 # and here.
#                 "javascript_origins": [],
#             }
#         }
#         return client_config
#
#     # The next step here is to implement get_authorization_url
#     # Reference:
#     # https://developers.google.com/identity/protocols/oauth2/web-server#creatingclient
#     def get_authorization_url(self):
#         redirect_uri = self._get_redirect_uri()
#         client_config = self._generate_client_config()
#
#         google_oauth_flow = google_auth_oauthlib.flow.Flow.from_client_config(
#             client_config=client_config, scopes=self.SCOPES
#         )
#         google_oauth_flow.redirect_uri = redirect_uri
#
#         authorization_url, state = google_oauth_flow.authorization_url(
#             access_type="offline",
#             include_granted_scopes="true",
#             prompt="select_account",
#         )
#         return authorization_url, state
#
#         # Code, unrelated to this example, below