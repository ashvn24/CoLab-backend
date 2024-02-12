from django.urls import path
from .views import *
urlpatterns = [
    path('login/',AdminLogin.as_view(), name='AdminLogin'),
    path('allUsers/',AdminUserList.as_view(),name='AllUsers'),
]
