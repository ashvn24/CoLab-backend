from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from .utils import send_Otp
from .models import Otp
from rest_framework.permissions import IsAuthenticated
from .task import send_mail_func

# Create your views here.


class RegisterUser(GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        user_data = request.data
        serializer = self.serializer_class(data=user_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.data
            send_Otp(user['email'])
            return Response({
                'data': user,
                'message': f'hii'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOtp(GenericAPIView):
    def post(self, request):
        otpCode = request.data.get('otp')
        try:
            user_code = Otp.objects.get(code=otpCode)
            user = user_code.user
            if not user.is_verified:
                user.is_verified = True
                user.save()
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


class LoginUser(GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class Profile(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = {
            'id': request.user.id,
            'name': request.user.username,
            'email': request.user.email,
            'msg': 'it works',
            'is_staff': request.user.is_staff,
            'is_superuser':request.user.is_superuser
            
        }
        send_mail_func.delay()
        return Response(data, status=status.HTTP_200_OK)

