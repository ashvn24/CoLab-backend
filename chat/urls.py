from . import views
from django.urls import path
from .views import *
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'signals', SignalViewSet, basename='signal')

urlpatterns = [
    path('user/<int:user_id1>/<int:user_id2>/', MessageListView.as_view(), name='chat-messages'),
    path('videoCall/', SignalViewSet.as_view({'get': 'list', 'post': 'create'}), name='video'), 
    # Specify allowed actions for the SignalViewSet
] + router.urls
