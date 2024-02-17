from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .Manger import UserManager
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import MultiPartParser, FormParser

# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add =True)
    
    USERNAME_FIELD="email"
    
    REQUIRED_FIELDS= []
    
    objects = UserManager()
    
    def __str__(self):
        return self.email
    
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh':str(refresh),  # str because simple jwt returns string not bytes
            'access': str(refresh.access_token)
            
        }
    
class Otp(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    code = models.CharField(max_length=5,unique=True)
    
    def __str__(self):
        return f"{self.user.email}-otp"
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    full_name = models.CharField(max_length = 200, blank= True)
    profile_image = models.ImageField( upload_to="profile/",blank=True)
    bio  = models.CharField(max_length= 300, blank= True)
    channel_link = models.CharField(max_length = 200, blank =True)
    
    
    def __str__(self):
        return f"{self.user.username}'s profile"

    
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    title = models.CharField(max_length=100,blank= False)
    description = models.TextField(blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    permission = models.BooleanField(default=False)

    def __str__(self):
        return self.title
class PostAttachment(models.Model): 
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='attachments' )
    files = models.FileField(upload_to= "posts/")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.post.title}"s post attachment"'
    