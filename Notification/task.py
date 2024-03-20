from celery import shared_task
from .models import Notification
from datetime import timedelta
from django.utils import timezone


@shared_task
def delete_accepted_notification():
    
    two_days_ago = timezone.now() - timedelta(days=2)

    notifications = Notification.objects.filter(
    message__icontains='has been accepted',
    timestamp__lte=two_days_ago
    )
    
    notifications.delete()
