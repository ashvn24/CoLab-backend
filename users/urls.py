from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/',RegisterUser.as_view(),name='register'),
    path('verify/',VerifyOtp.as_view(),name='verify'),
    path('login/',LoginUser.as_view(),name='login'),
    path('profile/',Profile.as_view(),name="user-profile"),
    path('token/refresh',TokenRefreshView.as_view(),name= 'token_refresh')  # for token refresh
]
