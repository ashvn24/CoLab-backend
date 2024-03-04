from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import *
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import generics, permissions, status
from .utils import send_Otp
from .models import Otp
from rest_framework.permissions import IsAuthenticated
from .task import send_mail_func, send_Accept_mail
from rest_framework_simplejwt.authentication import JWTAuthentication
import jwt
from django.conf import settings
from django.shortcuts import get_object_or_404


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
        user_id = self.request.data.get('id')
        if user_id:
            profile = UserProfile.objects.get(pk=user_id)
        else:
            user = request.user
            profile = UserProfile.objects.get(user=user)
        profile_serializer = UserProfileSerializer(profile)
        response_data = profile_serializer
        return Response(response_data.data, status=status.HTTP_200_OK)


class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostsSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        access_token = request.headers.get('Authorization')

        if access_token is None:
            raise AuthenticationFailed('Access token is required')

        try:
            token = access_token.split(' ')[1]
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']
            attachments_data = request.FILES.getlist('files')
            print('attach', attachments_data)
            post_data = request.data
            post_data.pop('files', None)

            serializer = self.get_serializer(data=post_data)
            serializer.is_valid(raise_exception=True)
            post_instance = serializer.save(user_id=user_id)

            for attachment_data in attachments_data:
                PostAttachment.objects.create(
                    files=attachment_data, user_id=user_id, post=post_instance)

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
        return Post.objects.all().order_by('-created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetPostDetail(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        post_id = self.kwargs.get('id')

        try:
            post = Post.objects.prefetch_related('attachments').get(pk=post_id)
        except Post.DoesNotExist:
            return Response({"error": "Post does not exist"}, status=status.HTTP_404_NOT_FOUND)
        print(request.user)
        if post.user == request.user:  # Creator of the post
            serializer = PostSerializer(post)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Check if the user is an editor and if the request is accepted
        user = request.user
        if EditorRequest.objects.filter(editor=user, post=post, accepted=True).exists():
            serializer = PostSerializer(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # If the user is an editor but request is not accepted, return limited details
            serializer = PosSerializer(post)
            return Response(serializer.data, status=status.HTTP_200_OK)


class GetMyPost(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get(self, request):
        access_token = request.headers.get('Authorization')

        if access_token is None:
            raise AuthenticationFailed('Access token is required')

        try:
            token = access_token.split(' ')[1]
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']
            post = Post.objects.filter(user=user_id).order_by("-created_at")
            serializer = self.get_serializer(post, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Post.DoesNotExist:
            return Response({'message': 'No posts found'}, status=status.HTTP_404_NOT_FOUND)


class PostUpdateView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostsSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        access_token = request.headers.get('Authorization')

        if access_token is None:
            raise AuthenticationFailed('Access token is required')

        try:
            token = access_token.split(' ')[1]
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']
            attachments_data = request.FILES  # Create a mutable copy of request.FILES
            post_data = request.data.copy()  # Create a mutable copy of request.data
            post_data.pop('files', None)

            instance = self.get_object()  # Retrieve the existing post object
            serializer = self.get_serializer(instance, data=post_data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user_id=user_id)  # Save the updated post data

            # Update attachments
            if attachments_data:
                for attachment_data in attachments_data.getlist('files'):
                    PostAttachment.objects.create(
                        files=attachment_data, user_id=user_id, post=instance)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Access token has expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid access token')


class UserProfileUpdateAPIView(generics.UpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    # Change this to the appropriate field name used for lookup (e.g., 'user_id')
    lookup_field = 'pk'

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class EditorRequestCreateAPIView(generics.CreateAPIView):
    queryset = EditorRequest.objects.all()
    serializer_class = EditorRequestSerializer

    def create(self, request, *args, **kwargs):
        access_token = request.headers.get('Authorization')
        token = access_token.split(' ')[1]
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = payload['user_id']
        # editor_id = request.data.get('editor')
        post_id = request.data.get('post')

        editor = get_object_or_404(User, pk=user_id)
        post = get_object_or_404(Post, pk=post_id)

        # Create the editor request instance
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(editor=editor, post=post)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Return a response indicating that the request has been sent to the post creator


class CreatorEditorRequestsAPIView(generics.ListAPIView):
    serializer_class = EditRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter the editor requests related to the posts created by the current user
        return EditorRequest.objects.filter(post__user=self.request.user).order_by("-created_at")


class AcceptEditorRequestAPIView(generics.RetrieveUpdateAPIView):
    queryset = EditorRequest.objects.all()
    serializer_class = EditorRequestSerializer

    def update(self, request, *args, **kwargs):
        editor_request_id = request.data.get('id')
        print(editor_request_id)

        try:
            # Retrieve the EditorRequest object
            instance = EditorRequest.objects.get(id=editor_request_id)

            # Update the 'accepted' field to True
            instance.accepted = True
            instance.save()
            send_Accept_mail.delay()

            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except EditorRequest.DoesNotExist:
            return Response({"message": "EditorRequest does not exist"}, status=status.HTTP_404_NOT_FOUND)


class AcceptedPostsListView(generics.ListAPIView):
    serializer_class = EditRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Check if 'id' exists in request.data
        if 'id' in self.kwargs:
            user_id = self.kwargs['id']
            print(user_id)
            # Find the user object based on the provided user_id
            try:
                user = User.objects.get(id=user_id)
                print(user)
            except User.DoesNotExist:
                # Handle case where user does not exist
                return EditorRequest.objects.none()

            # Check if the user is the same as the request user or the authenticated user
            if user.role == 'creator':
                return EditorRequest.objects.filter(
                    accepted=True,  # Filter for accepted requests
                    post__user=user  # Filter for posts where the user is the requested user
                ).distinct('editor')
            else:
                print(user)
                return EditorRequest.objects.filter(
                    accepted=True,  # Filter for accepted requests
                    editor=user  # Filter for posts where the user is the requested user
                ).distinct('post__user')
        else:
            # Perform the original query if 'id' does not exist in request.data
            return EditorRequest.objects.filter(editor=self.request.user, accepted=True)


class RejectRequestView(generics.DestroyAPIView):
    queryset = EditorRequest.objects.all()
    serializer_class = EditorRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        req_id = self.request.data.get('id')

        if req_id is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            instance = EditorRequest.objects.get(id=req_id)
            return instance
        except EditorRequest.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if isinstance(instance, Response):
            return instance  # Return the response if it's not an instance

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostDeleteAPIView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # You can adjust the permissions as needed
    permission_classes = [IsAuthenticated]

    def get_object(self):
        post_id = self.request.data.get('id')
        print(post_id)
        if post_id is None:
            return Response({"message": "Post id not provided in request data"}, status=status.HTTP_404_NOT_FOUND)

        try:
            post = Post.objects.get(id=post_id, user=self.request.user)
            self.check_object_permissions(self.request, post)
            return post
        except Post.DoesNotExist:
            return Response("Post does not exist")

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)


class PostDelete(generics.DestroyAPIView):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def delete(self, request, *args, **kwargs):
        post_id = self.kwargs.get('id')
        print(post_id)
        if not post_id:
            return Response("ERROR-NOID", status=status.HTTP_400_BAD_REQUEST)

        try:
            post = Post.objects.get(id=post_id, user=self.request.user)
        except Post.DoesNotExist:
            return Response("POST_DOES_NOT_EXIST", status=status.HTTP_404_NOT_FOUND)

        self.perform_destroy(post)
        return Response("Deleted", status=status.HTTP_200_OK)
