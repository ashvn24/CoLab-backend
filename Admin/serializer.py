from rest_framework import serializers
from users.models import User
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

class AdminLoginSerializer(serializers.ModelSerializer): 
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'access_token', 'refresh_token']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        request = self.context.get('request')
        user = authenticate(request, email=email, password=password)
        
        if not user:
            raise AuthenticationFailed("Invalid credentials")
        
        if not user.is_verified:
            raise AuthenticationFailed("Account not verified")
        
        if not user.is_superuser:
            raise AuthenticationFailed("You are not authorized to log in as an admin")

        user_token = user.tokens()
        return {
            'email': user.email,
            'access_token': str(user_token.get('access')),
            'refresh_token': str(user_token.get('refresh')),
        }