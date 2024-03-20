from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from users.models import EditorRequest, User
from .models import Notification
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import NotificationSerializer


class NotificationList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer
    
    def get_queryset(self):
        user_id = self.request.query_params.get('user_id', None)
        print(user_id)
        if user_id is not None:
            queryset = Notification.objects.filter(user=user_id)
            return queryset
        else:
            return Notification.objects.none()