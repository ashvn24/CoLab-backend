from django.urls import path
from .views import NotificationList

urlpatterns = [
    path('notifList/', NotificationList.as_view(), name='notiflist'),
]
