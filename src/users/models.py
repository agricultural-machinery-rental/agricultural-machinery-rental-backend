from django.contrib.auth.models import AbstractUser
from django.db import models

# Перечень ролей, корректируется при необходимости
ADMIN = "admin"
MODERATOR = "moderator"
USER = "user"
ROLES = [
    (ADMIN, "Админ"),
    (MODERATOR, "Модератор"),
    (USER, "Пользователь"),
]


class User(AbstractUser):
    """
    Переопределенный пользователь
    """

    first_name = models.CharField(
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
    role = models.CharField(
        max_length=20, choices=ROLES, verbose_name="Роль", default=USER
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR
