import random;
from django.core.mail  import EmailMessage
from .models import *
from django.conf import settings

def generateOtp():
    otp=""
    for i in range(4):
        otp+=str(random.randint(1,9))
    return otp

def send_Otp(email):
    Subject = "One Time Password"
    otp_code = generateOtp()
    print(otp_code)
    user = User.objects.get(email=email)
    email_body = f"hii {user.username} thanks for signing up on CoLab please verify the account with otp{otp_code}"
    from_email = settings.DEFAULT_FROM_EMAIL
    
    Otp.objects.create(user=user, code=otp_code)
    
    send_mail = EmailMessage(subject=Subject, body=email_body, from_email=from_email, to=[email])
    send_mail.send(fail_silently=True)