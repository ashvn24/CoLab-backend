from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import *
from users.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class AdminLogin(GenericAPIView):
    serializer_class = AdminLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class AdminUserList(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        if not request.user.is_superuser:
            return Response({"error": "Unauthorized access"}, status=status.HTTP_401_UNAUTHORIZED)

        users = User.objects.filter(is_staff=False)
        serializers = AdminUserListSerializer(users, many=True)
        return Response(serializers.data, status= status.HTTP_200_OK)

    def post(self,request):
        user_id = request.data.get('user_id')
        user = User.objects.get(id=user_id)
        
        if not user:
            return Response({'error':"User Not Found"},status=status.HTTP_400_BAD_REQUEST)
        
        if user.is_active:
            user.is_active = False
        else:
            user.is_active = True
        
        user.save()
        
        return Response(status=status.HTTP_200_OK)
        