from django.db import models


class Role(models.IntegerChoices):
    ADMIN = 1
    MANAGER = 2
    USER = 3


class Category(models.IntegerChoices):
    TRACTORS = 1, "Трактора"
    COMBINES = 2, "Комбайны"
    EQUIPMENT_SOWING = 3, "Посевная техника"
    MOTORIZED_TRACTORS = 4, "Мототракторы"
    TRAILERS = 5, "Прицепы"
    PLOWS = 6, "Плуги"
    LIFT_TRUCKS = 7, "Погрузчики"
    ATTACHMENTS = 8, "Навесное оборудование"


class ReservationStatusOptions(models.IntegerChoices):
    CREATED = 0, "Создан"
    CONFIRMED = 1, "Подтвержден"
    CANCELLED = 2, "Отменен"
    AT_WORK = 3, "В работе"
    FINISHED = 4, "Завершен"


BOOLEAN_CHOICES = (
    (0, False),
    (1, True),
)
