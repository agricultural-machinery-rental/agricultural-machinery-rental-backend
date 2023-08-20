import re
from django.core.exceptions import ValidationError


from core.enums import Limits


def check_names(value):
    if re.search("[а-яА-ЯёЁ]", value) is None:
        raise ValidationError(
            "Имя пользователя должно состоять из букв " "кирилицы"
        )
    if len(value) < 2:
        raise ValidationError("Имя пользователя не может быть 1 символом")


def check_password(value):
    if not re.findall("\d", value):
        raise ValidationError("Пароль должен содержать хотя бы одну цифру")
    if not re.findall("[A-Z]", value):
        raise ValidationError(
            ("The password must contain at least 1 uppercase letter, A-Z."),
        )
    if not re.findall("[a-z]", value):
        raise ValidationError(
            ("The password must contain at least 1 lowercase letter, a-z."),
        )
    if not re.findall("[()[\]{}|\\`~!@#$%^&*_\-+=;:'\",<>./?]", value):
        raise ValidationError(
            (
                "Пароль должен содержать как минимум 1 символ: "
                "()[]{}|\`~!@#$%^&*_-+=;:' \",<>./?"
            ),
        )
    if len(value) < Limits.MIN_LENGTH_PASS:
        raise ValidationError(
            ("Пароль должен содержать не меньше 8 символов"),
        )
    if len(value) > Limits.MAX_LENGTH_PASS:
        raise ValidationError(
            ("Пароль должен содержать не больше 25 символов"),
        )
    if re.findall("[А-Яа-яёЁ]", value):
        raise ValidationError(
            ("Кирилица не допустима в пароле"),
        )
