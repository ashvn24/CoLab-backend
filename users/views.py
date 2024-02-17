from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import *
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import generics, permissions, status
from .utils import send_Otp
from .models import Otp
from rest_framework.permissions import IsAuthenticated
from .task import send_mail_func
from rest_framework_simplejwt.authentication import JWTAuthentication
import jwt
from django.conf import settings



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
    


class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    
    print('permissioncls',permission_classes)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        access_token = request.headers.get('Authorization')

        if access_token is None:
            raise AuthenticationFailed('Access token is required')

        try:
            token = access_token.split(' ')[1]
            payload = jwt.decode(token, settings.SECRET_KEY , algorithms=['HS256'])
            user_id = payload['user_id']
            print(user_id)
            attachments_data = request.FILES.getlist('files')
            post_data = request.data.copy()
            post_data.pop('files', None)

            serializer = self.get_serializer(data=post_data)
            serializer.is_valid(raise_exception=True)
            post_instance = serializer.save(user_id=user_id)

            for attachment_data in attachments_data:
                PostAttachment.objects.create(files=attachment_data, user_id=user_id, post=post_instance)

            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Access token has expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid access token')
        
class AllPostsListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Return all posts
        return Post.objects.all()
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
class GetPostDetail(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        post = request.data.get('post_id')
        try:
            instance = Post.objects.prefetch_related('attachments').get(pk=post)
            serializer = PostSerializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK )
        
        except Post.DoesNotExist:
            return Response({"error": "Post does not exist"},  
                           status=status.HTTP_404_NOT_FOUND)
            
            
            
          

# to get all post along with their respected attachments

# class AllPostsListView(generics.ListAPIView):
#     serializer_class = PostSerializer
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return Post.objects.all()

#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         serializer = self.get_serializer(queryset, many=True)
#         data = serializer.data

#         for post_data in data:
#             post_id = post_data['id']
#             post_attachments = PostAttachment.objects.filter(post_id=post_id)
#             attachment_serializer = PostAttachmentSerializer(post_attachments, many=True)
#             post_data['attachments'] = attachment_serializer.data

#         return Response(data)



 # create post without accessing user from jwt   
    
# class PostCreateView(generics.CreateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

#     def create(self, request, *args, **kwargs):
#         attachments_data = request.FILES.getlist('files')
#         post_data = request.data.copy()
#         post_data.pop('files', None)

#         serializer = self.get_serializer(data=post_data)
#         serializer.is_valid(raise_exception=True)
#         post_instance = serializer.save()

#         for attachment_data in attachments_data:
#             PostAttachment.objects.create(files=attachment_data, user=request.user, post=post_instance)

#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)