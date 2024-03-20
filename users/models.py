from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .Manger import UserManager
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import MultiPartParser, FormParser

# Create your models here.

AUTH_PROVIDERS = {'email':'email', 'google': 'google'}
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add =True)
    auth_provider = models.CharField(max_length=100,default=AUTH_PROVIDERS.get('email'))
    
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
    instagram = models.CharField(max_length=150, null= True, blank=True)
    facebook = models.CharField(max_length= 150, null= True, blank=True)
    phone = models.CharField(max_length = 15, blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"

    
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    titleDesc = models.CharField(max_length=400,blank= False,null=True)
    title = models.CharField(max_length=300,blank= False)
    description = models.TextField( max_length=600, blank=True, null=True)
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
    
class EditorRequest(models.Model):
    editor = models.ForeignKey(User, related_name='editor_requests', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='editor_requests', on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    accepted_time = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.editor.username}"s Request"'
    
class SubmitWork(models.Model):
    editor = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    creator = models.ForeignKey(User, related_name='reciever', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    vidkey = models.CharField(max_length=200)
    desc = models.TextField(max_length=400,blank=True, null=True)
    Quatation = models.IntegerField()
    
    def __str__(self):
        return f'{self.editor.username}"s request to {self.creator.username}'
    

    