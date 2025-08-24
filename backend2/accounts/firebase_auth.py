import firebase_admin
from firebase_admin import credentials, auth as firebase_auth
from django.contrib.auth.models import User
from django.contrib.auth.backends import BaseBackend
from rest_framework import authentication
from rest_framework import exceptions
import os

# Initialize Firebase Admin SDK
cred = credentials.Certificate(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'serviceAccountKey.json'))
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)


class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None
        
        id_token = auth_header.split('Bearer ')[1]
        try:
            decoded_token = firebase_auth.verify_id_token(id_token)
            uid = decoded_token['uid']
            email = decoded_token.get('email', '')
            
            # Get or create user
            user, created = User.objects.get_or_create(
                username=uid,
                defaults={'email': email}
            )
            
            return (user, None)
        except Exception as e:
            raise exceptions.AuthenticationFailed('Invalid Firebase token')


class FirebaseAuthBackend(BaseBackend):
    def authenticate(self, request, firebase_uid=None, **kwargs):
        if firebase_uid is None:
            return None
        
        try:
            user = User.objects.get(username=firebase_uid)
            return user
        except User.DoesNotExist:
            return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None