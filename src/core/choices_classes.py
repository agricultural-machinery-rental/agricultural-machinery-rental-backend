from django.db import models


class Role(models.IntegerChoices):
    ADMIN = 1
    MODERATOR = 2
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
    CREATED = 0
    CONFIRMED = 1
    CANCELLED = 2
    AT_WORK = 3
    FINISHED = 4
