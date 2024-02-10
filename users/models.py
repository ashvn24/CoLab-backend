from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .Manger import UserManager
from rest_framework_simplejwt.tokens import RefreshToken
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