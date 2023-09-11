from django.contrib.auth.base_user import BaseUserManager

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
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                "Суперпользователь должен иметь is_superuser=True"
            )

        first_name = input("Введите имя: ")
        extra_fields.setdefault("first_name", first_name)
        last_name = input("Введите фамилию: ")
        extra_fields.setdefault("last_name", last_name)
        phone_number = input("Введите номер телефона: ")
        extra_fields.setdefault("phone_number", phone_number)
        extra_fields.setdefault("role", Role.ADMIN)

        return self.create_user(email, password, **extra_fields)

    def get_by_natural_key(self, email):
        return self.get(email=email)
