from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from users.models import EditorRequest, User
from .models import Notification

@receiver(post_save, sender=EditorRequest)
def create_editor_request_notification(sender, instance, created, **kwargs):
    if created:

        # Access the user associated with the post
        post_user = instance.post.user

        # Create a notification for the user associated with the post
        Notification.objects.create(
            user=post_user,  # Assuming Notification has a user field
            message=f'User {instance.editor.username} has requested for your post "{instance.post}"',
            timestamp=timezone.now()
        )
