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
    message = f"Hii {user.username} thanks for signing up on CoLab please verify the account with otp  :{otp_code}"
    from_email = settings.EMAIL_HOST_USER
    
    Otp.objects.create(user=user, code=otp_code)
    
    d_mail = EmailMessage(subject=Subject, body= message, from_email=from_email, to=[email])
    d_mail.send(fail_silently=True)