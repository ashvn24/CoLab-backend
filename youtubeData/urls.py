# urls.py
from django.urls import path
from .views import GetAnalytics,ChannelVideosView, VideoUploadView

urlpatterns = [
    path('getData/', GetAnalytics.as_view(), name='vdData'),
    path('chdata/',ChannelVideosView.as_view(),name='dta'),
    path('upload/', VideoUploadView.as_view(), name='video-upload'),

]
