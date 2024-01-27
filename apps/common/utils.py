import random
import uuid

from django.core.mail import EmailMessage
from django.template.loader import get_template
from apps.product.models import CartItem, Order
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


def get_order_id():
    """
    this method is used to return an order id
    """
    order_id = 'ORD_ID' + generate_otp()
    if not Order.objects.filter(order_id=order_id).exists():
        return order_id
    return get_order_id()


def get_combine_order_id():
    combine_order_id = uuid.uuid4()
    if not Order.objects.filter(combine_order_id=combine_order_id).exists():
        return combine_order_id
    return get_combine_order_id()
