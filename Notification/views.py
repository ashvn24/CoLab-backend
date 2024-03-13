from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from users.models import EditorRequest, User
from .models import Notification
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import NotificationSerializer

# @receiver(post_save, sender=EditorRequest)
# def create_editor_request_notification(sender, instance, created, **kwargs):
#     if created:

#         # Access the user associated with the post
#         post_user = instance.post.user

#         # Create a notification for the user associated with the post
#         Notification.objects.create(
#             user=post_user,  # Assuming Notification has a user field
#             message=f'User {instance.editor.username} has requested for your post "{instance.post}"',
#             obj = instance,
#             timestamp=timezone.now()
#         )

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