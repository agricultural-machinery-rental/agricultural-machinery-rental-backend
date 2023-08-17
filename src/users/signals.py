import json
import requests

from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created

from config import settings


@receiver(reset_password_token_created)
def password_reset_token_created(
    sender, instance, reset_password_token, *args, **kwargs
):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    context = {
        "email": reset_password_token.user.email,
        "reset_password_url": "{}?token={}".format(
            instance.request.build_absolute_uri(
                reverse("password_reset:reset-password-confirm")
            ),
            reset_password_token.key,
        ),
        "token": reset_password_token.key,
    }

    # render email text
    email_html_message = render_to_string(
        "email/user_reset_password.html", context
    )
    email_plaintext_message = render_to_string(
        "email/user_reset_password.txt", context
    )
    subject = "Сброс пароля на {title}".format(title="АгроПарк")

    if settings.TRANSFER and not settings.EMAIL_FILE:
        url = settings.TRANSFER_SERVER
        data = {
            "emai_to": reset_password_token.user.email,
            "subject": subject,
            "body": email_html_message,
            "username": settings.EMAIL_HOST_USER,
            "password": settings.EMAIL_HOST_PASSWORD,
            "port": settings.EMAIL_PORT,
            "server": settings.EMAIL_HOST,
            "token": settings.TRANSFER_TOKEN,
        }
        response = requests.post(url, data=json.dumps(data))
        print(response.json())

    else:
        msg = EmailMultiAlternatives(
            # title:
            subject,
            # message:
            email_plaintext_message,
            # from:
            settings.EMAIL_HOST_USER,
            # to:
            [reset_password_token.user.email],
        )
        msg.attach_alternative(email_html_message, "text/html")
        msg.send()
