from django.db import models


class Role(models.IntegerChoices):
    ADMIN = 1
    MODERATOR = 2
    USER = 3


class Category(models.IntegerChoices):
    TRACTOR = 1  # Трактор
    COMBINE_HARVESTER = 2  # Комбайн
    EQUIPMENT_SOWING = 3  # Посевная техника
    PLOW = 4  # Плуг
    MOWING_GRASS = 5  # Покос травы
    SPRAYER = 6  # Опрыскиватель
    TRAILER = 7  # Прицеп
    DUMP_TRUCK = 8  # Самосвал
    LIFT_TRUCK = 9  # Погрузчик
