import uuid
from celery import shared_task
from .models import User
from django.core.mail import EmailMessage
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
from .models import EditorRequest
import boto3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.contrib import messages


@shared_task(bind=True)
def send_mail_func(self):
    users = User.objects.filter(is_superuser=False).order_by('-id').first()
    print(users)
    if users:
       
        sender_email = settings.EMAIL_HOST_USER
        receiver_email = users.email  # Assuming 'email' is defined somewhere in your code
        password = settings.EMAIL_HOST_PASSWORD
        subject = "Welecome to COLAB"
        message = (
            f"Hi {users.username},\n\n"
            f"Thank you for signing up on COLAB.\n"
            f"We're excited to have you join our Colab project, a collaborative platform designed to bridge the gap between editors and content creators. Our mission is to streamline the process of finding editors, reviewing work, and directly uploading media to YouTube channels.\n\n"
            "### Getting Started\n\n"
            "Here’s how you can make the most out of our platform:\n\n"
            "1. **For Editors:**\n"
            "   - Discover and connect with content creators looking for your expertise.\n"
            "   - Review and provide feedback on projects effortlessly.\n"
            "   - Enhance your portfolio with diverse projects.\n\n"
            "2. **For Content Creators:**\n"
            "   - Easily find skilled editors to bring your vision to life.\n"
            "   - Simplify the workflow from project initiation to final review.\n"
            "   - Directly upload your polished content to your YouTube channel.\n\n"
            "### Contact and Support\n\n"
            "If you have any questions or need assistance, our support team is here to help. Reach out to us at ashwinvk77@gmail.com.\n\n"
            "Thank you for joining us. We look forward to seeing the amazing collaborations that will emerge from our platform!\n\n"
            "Best regards,\n"
            "Colab Team"
        )

        try:
            # Create the email message
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'plain'))

            with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
                server.starttls()
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, msg.as_string())
        except smtplib.SMTPAuthenticationError:
            messages.error(
                 'Failed to send email. Please check your email configuration.')
        except Exception as e:
            messages.error( f'An error occurred: {str(e)}')
    else:
        messages.info( 'No accepted requests found.')

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

        sender_email = settings.EMAIL_HOST_USER
        receiver_email = latest_accepted_request.editor.email
        password = settings.EMAIL_HOST_PASSWORD
        subject = "Request Accepted"
        message = (
            f"Hi {editor},\n\n"
            f"Your request for the post '{post_title}' has been accepted by "
            f"{latest_accepted_request.post.user.username}!\n\n"
            "Best regards,\n"
            "colab Team"
        )
        try:
            # Create the email message
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'plain'))

            with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
                server.starttls()
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, msg.as_string())
        except smtplib.SMTPAuthenticationError:
            messages.error(
                 'Failed to send email. Please check your email configuration.')
        except Exception as e:
            messages.error( f'An error occurred: {str(e)}')
    else:
        messages.info( 'No accepted requests found.')
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
