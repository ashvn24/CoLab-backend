import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from channels.db import database_sync_to_async
from users.models import  User

class JwtAuthentication(BaseAuthentication):
    
    @database_sync_to_async
    def authenticate_websocket(self,scope,token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            
            user_id = payload['user_id']
            user = User.objects.get(id=user_id)
            
            return user
        except User.DoesNotExist:
            raise AuthenticationFailed("Unauthenticated")