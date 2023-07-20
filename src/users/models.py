from django.contrib.auth.models import AbstractUser
from django.db import models

from core.choices_classes import Role


class User(AbstractUser):
    """
    Переопределенный пользователь
    """

    full_name = models.CharField(
        verbose_name="Фамилия и имя",
        max_length=150,
        blank=False,
        null=False,
    )
    email = models.EmailField(
        verbose_name="Адрес электронной почты",
        blank=False,
        null=False,
        unique=True,
    )
    role = models.IntegerField(
        verbose_name="Роль",
        max_length=20,
        choices=Role.choices,
        default=Role.USER,
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    @property
    def is_admin(self):
        return self.role == Role.ADMIN

    @property
    def is_moderator(self):
        return self.role == Role.MODERATOR
