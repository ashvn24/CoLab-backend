from django.urls import path
from .views import *


urlpatterns = [
    path('register/',RegisterUser.as_view(),name='register'),
    path('verify/',VerifyOtp.as_view(),name='verify'),
    path('login/',LoginUser.as_view(),name='login'),
    path('profile/',Profile.as_view(),name="user-profile"),
]
