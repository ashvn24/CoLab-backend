from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/',RegisterUser.as_view(),name='register'),
    path('verify/',VerifyOtp.as_view(),name='verify'),
    path('login/',LoginUser.as_view(),name='login'),
    path('profile/',Profile.as_view(),name="user-profile"),
    path('token/refresh',TokenRefreshView.as_view(),name= 'token_refresh'),  # for token refresh
    path('create_post/',PostCreateView.as_view(), name='create_post'),
    path('all_post/',AllPostsListView.as_view(),name='all_post'),
    path('get_post/',GetPostDetail.as_view(),name='get_post'),
    path('get_mypost/',GetMyPost.as_view(),name='get_Mypost'),
]

