import random
from django.core.mail import EmailMessage
from django.template.loader import get_template
from apps.product.models import CartItem
from exclusive import settings


def get_total_bill(user_id):
    """
    this method is used to get a total billed
    :param user_id
    return total billed
    """
    total_bill = 0
    cart_obj = CartItem.objects.filter(user_id=user_id)
    if cart_obj:
        for cart in cart_obj:
            sub_price = cart.quantity * cart.product.price
            total_bill += sub_price
    return total_bill


def send_otp(data):
    """
    this method is used to send an OTP on email
    :param data
    """
    six_digit_otp = generate_otp()
    data['otp'] = six_digit_otp
    email_data = {
        'subject': 'Exclusive verify email! OTP',
        'to_email': data['email'],
        'from_email': settings.EMAIL_HOST_USER,
        'detail': data
    }
    common_send_email(email_data, 'account/verify_otp.html')


def send_welcome_email(data):
    """
    this method is used to send a welcome email
    :param data
    """
    email_data = {
        'subject': 'Welcome to Exclusive family',
        'to_email': data['email'],
        'from_email': settings.EMAIL_HOST_USER,
        'detail': data
    }
    common_send_email(email_data, 'account/welcome_email.html')


def common_send_email(email_data, template):
    """
    common method to send email
    """
    ctx = dict()
    ctx['detail'] = email_data['detail']
    mail = EmailMessage(
        subject=email_data['subject'],
        body=get_template(template).render(ctx),
        from_email=settings.EMAIL_HOST_USER,
        to=[email_data['to_email']],
        reply_to=[settings.EMAIL_HOST_USER],

    )
    mail.content_subtype = "html"
    mail.send()


def generate_otp():
    return ''.join(str(random.choice(range(10))) for _ in range(6))
