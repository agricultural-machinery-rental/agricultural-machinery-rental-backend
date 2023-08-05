from importlib.resources import _

from django.db import models


class Role(models.IntegerChoices):
    ADMIN = 1
    MODERATOR = 2
    USER = 3


class Category(models.IntegerChoices):
    TRACTORS = 1, _("Трактор")
    COMBINES = 2, _("Комбайны")
    EQUIPMENT_SOWING = 3, _("Посевная техника")
    MOTORIZED_TRACTORS = 4, _("Мототракторы")
    TRAILERS = 5, _("Прицепы")
    PLOWS = 6, _("Плуги")
    LIFT_TRUCKS = 7, _("Погрузчики")
    ATTACHMENTS = 8, _("Навесное оборудование")


class ReservationStatusOptions(models.IntegerChoices):
    CREATED = 0
    CONFIRMED = 1
    CANCELLED_BY_CLIENT = 2
    CANCELLED_BY_MANAGER = 3
    AT_WORK = 4
    FINISHED = 5
