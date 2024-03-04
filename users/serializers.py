from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','password','role','username','date_joined']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            
            instance.set_password(password)
        instance.save()
        return instance
    
class LoginUserSerializer(serializers.ModelSerializer): 
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)
    role = serializers.CharField(max_length=100, read_only=True)
    username =serializers.CharField(max_length=100, read_only= True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'access_token', 'refresh_token', 'role','username','user']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        request = self.context.get('request')
        user = authenticate(request, email=email, password=password)
        if not user:
            raise AuthenticationFailed("Invalid credentials")
        if not user.is_verified:
            raise AuthenticationFailed("Account not verified")
        if not user.is_active:
            raise AuthenticationFailed("User Blocked!")
        user_token = user.tokens()
        return {
            'email': user.email,
            'access_token': str(user_token.get('access')),
            'refresh_token': str(user_token.get('refresh')),
            'role': user.role,
            'username':user.username
        }

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer() 
    class Meta:
        model= UserProfile
        fields='__all__'
        
class PostAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostAttachment
        fields = '__all__'
        
class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Include the UserSerializer directly
    attachments = PostAttachmentSerializer(many=True, required=False)
    class Meta:
        model = Post
        fields = '__all__'
        
class PostsSerializer(serializers.ModelSerializer):
    attachments = PostAttachmentSerializer(many=True, required=False)
    class Meta:
        model = Post
        exclude =['user']
class PosSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Post
        fields = '__all__'
        
        
class EditorRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = EditorRequest
        fields = ['id', 'post', 'accepted']
        
class EditRequestSerializer(serializers.ModelSerializer):
    editor = UserSerializer()
    post = PostSerializer()

    class Meta:
        model = EditorRequest
        fields = ['id', 'editor', 'post', 'accepted']
        
    def get_req_count(self,obj):
        return len(obj.all(accepted=False))