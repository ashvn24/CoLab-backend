import random;
from django.core.mail  import EmailMessage
from .models import *
from django.conf import settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.contrib import messages

def generateOtp():
    otp=""
    for i in range(4):
        otp+=str(random.randint(1,9))
    return otp

def send_Otp(email):
    Subject = "One Time Password"
    otp_code = generateOtp()
    print(otp_code)
    if otp_code:
        
        user = User.objects.get(email=email)
        Otp.objects.create(user=user, code=otp_code)
        
        sender_email = settings.EMAIL_HOST_USER
        receiver_email = email
        password = settings.EMAIL_HOST_PASSWORD
        subject = "Your OTP Code"
        message = (
            f"Hi {user.username},\n\n"
            f"Your OTP code is {otp_code}. Please use this code to complete your verification.\n\n"
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