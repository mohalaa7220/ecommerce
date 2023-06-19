import random
from users.models import User
from django.core.mail import send_mail
from django.conf import settings
settings.DEFAULT_FROM_EMAIL,


def email_send(name, email):
    send_mail(
        'Booking for Hotel',
        f'Hallo dear, {name} your booking is recived we will call you as soon as',
        'from@example.com',
        [email],
        fail_silently=False,
    )


def send_otp_via_email(email):
    subject = 'Reset Password'
    otp = random.randint(1000, 9999)
    message = f'Your code is {otp}'
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, [email])
    user_obj = User.objects.get(email=email)
    user_obj.otp = otp
    user_obj.save()
