from celery import shared_task
from .models import User
from django.core.mail  import EmailMessage
from django.conf import settings

@shared_task(bind=True)

def send_mail_func(self):
    users = User.objects.filter(is_superuser=False).order_by('-id').first()
    print(users)
    if users:
        Subject = "Welcome to CoLab"
        message = f"Hii {users.username} thanks for signing up on CoLab "
        from_email = settings.EMAIL_HOST_USER
        
        d_mail = EmailMessage(subject=Subject, body= message, from_email=from_email, to=[users.email])
        d_mail.send(fail_silently=True)
    return 'done'