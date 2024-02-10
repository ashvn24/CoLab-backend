from celery import shared_task
from .models import User
# from django.core.mail import send_mail
from django.core.mail  import EmailMessage
from django.conf import settings

@shared_task(bind=True)

def send_mail_func(self):
    users = User.objects.filter(is_superuser=False).order_by('-id').first()
    if users:
        mail_subject = 'Hello'
        message = 'helooooo'
        to_email = users.email
        # Send email to the user
        # send_mail(
        #     subject=mail_subject,
        #     message=message,
        #     from_email=settings.EMAIL_HOST_USER,
        #     recipient_list=[to_email],
        #     fail_silently=True
        # )
        send_mail = EmailMessage(subject=mail_subject, body=message, from_email=settings.DEFAULT_FROM_EMAIL, to=[to_email])
        send_mail.send(fail_silently=True)
    return 'done'