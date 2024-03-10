# urls.py
from django.urls import path
from .views import GetAnalytics

urlpatterns = [
    path('getData/', GetAnalytics.as_view(), name='vdData'),
]
