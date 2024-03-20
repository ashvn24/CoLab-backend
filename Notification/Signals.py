from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Notification
from users.models import EditorRequest,SubmitWork
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.core.serializers import serialize

@receiver(post_save, sender=EditorRequest)
def create_editor_request_notification(sender, instance, created, **kwargs):
    if created:
        post_user = instance.post.user  # Get the user associated with the post
        message = f'{instance.editor.username} has requested for your post "{instance.post}"'
        Notification.objects.create(user=post_user, message=message, timestamp=timezone.now(), obj=instance)

        channel_layer = get_channel_layer()
        serialized_instance = serialize('json', [instance])
        async_to_sync(channel_layer.group_send)(
            'notifications_group',
            {
                'type': 'send_notification',
                'notification': {
                    'id': instance.id,
                    'message': message,
                    'timestamp': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'post': serialized_instance,
                },
                'recipient_user_id': post_user.id
            }
        )

@receiver(post_save, sender=EditorRequest)
def create_editor_request_accepted_notification(sender, instance, **kwargs):
    if instance.accepted:
        editor = instance.editor
        message = f'Your request for the post "{instance.post}" has been accepted.'
        Notification.objects.create(user=editor, message=message, timestamp=timezone.now(), obj=instance)

        channel_layer = get_channel_layer()
        serialized_instance = serialize('json', [instance])
        async_to_sync(channel_layer.group_send)(
            'notifications_group',
            {
                'type': 'send_notification',
                'notification': {
                    'id': instance.id,
                    'message': message,
                    'timestamp': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'post': serialized_instance,
                },
                'recipient_user_id': editor.id
            }
        )

@receiver(post_save,sender=SubmitWork)
def  submitwork_created(sender, instance, created, **kwargs):
    if created:
        reciever = instance.creator
        message = f'{instance.editor.username} has submitted a request for approval of your post {instance.post.title}'
        Notification.objects.create(user=reciever, message=message, timestamp=timezone.now(), work=instance)
        
        channel_layer = get_channel_layer()
        serialized_instance = serialize('json', [instance])
        async_to_sync(channel_layer.group_send)(
            'notifications_group',
            {
                'type': 'send_notification',
                'notification': {
                    'id': instance.id,
                    'message': message,
                    'timestamp': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'post': serialized_instance,
                },
                'recipient_user_id': reciever.id
            }
        )