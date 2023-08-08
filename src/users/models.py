from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from core.choices_classes import Role
from core.enums import Limits
from users.managers import UserManager


class User(AbstractUser):
    """
    Переопределенный пользователь
    """

    username = None
    email = models.EmailField(
        verbose_name="Адрес электронной почты",
        blank=False,
        null=False,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name="Имя",
        max_length=Limits.MAX_LENGTH_FIRST_NAME.value,
        blank=False,
        null=False,
    )
    last_name = models.CharField(
        verbose_name="Фамилия",
        max_length=Limits.MAX_LENGTH_LAST_NAME.value,
        blank=False,
        null=False,
    )
    patronymic = models.CharField(
        verbose_name="Отчество",
        max_length=Limits.MAX_LENGTH_PATRONYMIC.value,
        blank=True,
        null=True,
    )
    phone_number = PhoneNumberField(
        verbose_name="Номер телефона",
        max_length=Limits.MAX_LENGTH_PHONE_NUMBER.value,
        blank=False,
        null=False,
        unique=True,
    )
    role = models.IntegerField(
        verbose_name="Роль",
        choices=Role.choices,
        default=Role.USER,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return (
            f"{self.last_name} {self.first_name[0].upper()}."
            f"{self.patronymic[0] + '.' if self.patronymic else ''} "
        )

    @property
    def is_admin(self):
        return self.role == Role.ADMIN

    @property
    def is_moderator(self):
        return self.role == Role.MODERATOR


class Callback(models.Model):
    """
    Обратный звонок.
    """

    phone_number = PhoneNumberField(
        verbose_name="Номер телефона",
        max_length=Limits.MAX_LENGTH_PHONE_NUMBER.value,
        blank=False,
        null=False,
    )
    comment = models.CharField(
        verbose_name="Комментарий",
        max_length=Limits.MAX_LENGTH_COMMENT.value,
        blank=True,
        null=True,
    )
    is_finished = models.BooleanField(
        verbose_name="Завершено",
        default=False,
    )
    time_create = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True,
    )
    time_finished = models.DateTimeField(
        verbose_name="Дата завершения",
        auto_now=True,
    )

    class Meta:
        verbose_name = "Обратный звонок"
        verbose_name_plural = "Обратные звонки"
        default_related_name = "callback"

    def __str__(self) -> str:
        return f"{self.phone_number}"
