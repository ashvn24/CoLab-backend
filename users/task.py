from celery import shared_task
from .models import User
from django.core.mail import EmailMessage
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
from .models import EditorRequest


@shared_task(bind=True)
def send_mail_func(self):
    users = User.objects.filter(is_superuser=False).order_by('-id').first()
    print(users)
    if users:
        Subject = "Welcome to CoLab"
        message = f"Hii {users.username} thanks for signing up on CoLab "
        from_email = settings.EMAIL_HOST_USER

        d_mail = EmailMessage(subject=Subject, body=message,
                              from_email=from_email, to=[users.email])
        d_mail.send(fail_silently=True)
    return 'done'


@shared_task(bind=True)
def send_Accept_mail(self):
    latest_accepted_request = EditorRequest.objects.filter(
    accepted=True
    ).order_by('-created_at').first()

    # Check if there is an accepted request
    if latest_accepted_request:
        editor = latest_accepted_request.editor.username
        post_title = latest_accepted_request.post.title
        
        Subject = "Request Accepted"
        message = f"Hii {editor} Your request for the post-{post_title} has been Accepted by {latest_accepted_request.post.user.username}!"
        from_email = settings.EMAIL_HOST_USER

        d_mail = EmailMessage(subject=Subject, body=message,
                              from_email=from_email, to=[latest_accepted_request.editor.email])
        d_mail.send(fail_silently=True)
    return 'done'


@shared_task
def delete_old_accepted_requests():
    # Define the time diffrence
    threshold_time = timezone.now() - timedelta(days=1)

    # Filter EditorRequest instances with accepted=True and created_at older than threshold_time
    old_accepted_requests = EditorRequest.objects.filter(
        accepted=True, created_at__lte=threshold_time)
    print(old_accepted_requests)

    # Delete the filtered instances
    old_accepted_requests.delete()
