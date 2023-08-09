from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created

from config.settings import EMAIL_HOST_USER


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

    msg = EmailMultiAlternatives(
        # title:
        "Сброс пароля на {title}".format(title="АгроПарк"),
        # message:
        email_plaintext_message,
        # from:
        EMAIL_HOST_USER,
        # to:
        [reset_password_token.user.email],
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()
