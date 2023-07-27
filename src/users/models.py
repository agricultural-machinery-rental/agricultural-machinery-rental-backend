from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from core.choices_classes import Role


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Суперпользователь должен иметь is_staff=True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                "Суперпользователь должен иметь is_superuser=True"
            )

        first_name = input("Введите имя: ")
        extra_fields.setdefault("first_name", first_name)
        last_name = input("Введите фамилию: ")
        extra_fields.setdefault("last_name", last_name)
        extra_fields.setdefault("role", Role.ADMIN)

        return self.create_user(email, password, **extra_fields)

    def get_by_natural_key(self, email):
        return self.get(email=email)


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
        max_length=50,
        blank=False,
        null=False,
    )
    last_name = models.CharField(
        verbose_name="Фамилия",
        max_length=50,
        blank=False,
        null=False,
    )
    patronymic = models.CharField(
        verbose_name="Отчество",
        max_length=50,
        blank=True,
        null=True,
    )
    phone_number = models.CharField(
        verbose_name="Номер телефона",
        max_length=15,
        blank=False,
        null=False,
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
