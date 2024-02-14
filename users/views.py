from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from .utils import send_Otp
from .models import Otp
from rest_framework.permissions import IsAuthenticated
from .task import send_mail_func
from rest_framework import generics

# Create your views here.


class RegisterUser(generics.CreateAPIView):
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        send_Otp(user.email)
    
    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        username = request.data.get('username')
        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        response = super().create(request, *args, **kwargs)
        return Response({
            'data': response.data,
            'message': 'account created successfully'
        }, status=status.HTTP_201_CREATED)


class VerifyOtp(GenericAPIView):
    def post(self, request):
        otpCode = request.data.get('otp')
        print(otpCode)
        try:
            user_code = Otp.objects.get(code=otpCode)
            user = user_code.user
            if not user.is_verified:
                user.is_verified = True
                user.save()
                send_mail_func.delay()
                return Response({
                    'message': 'account created'
                }, status=status.HTTP_200_OK)
            return Response({
                'message': 'code is invalid'
            }, status=status.HTTP_204_NO_CONTENT)

        except Otp.DoesNotExist:
            return Response({
                'message': 'passcode not provided'
            }, status=status.HTTP_404_NOT_FOUND)


class LoginUser(generics.CreateAPIView):
    serializer_class = LoginUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class Profile(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        profile = UserProfile.objects.get(user=user)

        user_serializer = UserSerializer(user)
        profile_serializer = UserProfileSerializer(profile)

        response_data = {
            'user': user_serializer.data,
            'profile': profile_serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)

