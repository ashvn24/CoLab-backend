import requests
from google.oauth2 import id_token
from .models import User
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed


class Google():
    @staticmethod
    def validate(access_token):
        url = 'https://www.googleapis.com/oauth2/v1/userinfo'
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Accept': 'application/json'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            user_info = response.json()
            return user_info
        else:
            # Handle error responses
            print(f"Error: {response.status_code}")
            return None
        
def register_social_user(provider,email,username):
    user = User.objects.filter(email=email)
    if user.exists():
        if provider == user[0].auth_provider:
            login_user = authenticate(email=email, password= settings.SOCIAL_AUTH_PASSWORD)
            user_token = login_user.tokens()
            return {
                'email': login_user.email,
                'access_token': str(user_token.get('access')),
                'refresh_token': str(user_token.get('refresh')),
                'role': login_user.role,
                'username':login_user.username
            }
        else:
            raise AuthenticationFailed(
                detail=f'This account already linked with another provider'  
            )
    new_user = {
        'email':email,
        'username':username,
        'role':'Editor',
        'password':settings.SOCIAL_AUTH_PASSWORD
    }
    register_user = User.objects.create(**new_user)
    
    register_user.auth_provider = provider
    register_user.is_verified= True
    register_user.is_active = True
    register_user.set_password(settings.SOCIAL_AUTH_PASSWORD)
    register_user.save()
    login_user = authenticate(email=email, password = settings.SOCIAL_AUTH_PASSWORD)
    print('---login',login_user)
    user_token = login_user.tokens()
    return {
            'email': login_user.email,
            'access_token': str(user_token.get('access')),
            'refresh_token': str(user_token.get('refresh')),
            'role': login_user.role,
            'username':login_user.username
        }