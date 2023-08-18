from django.contrib.auth import settings
from django.db import models

from core.choices_classes import Category


class MachineryBrandname(models.Model):
    brand = models.CharField(
        verbose_name="Марка техники", max_length=100, blank=False, null=False
    )

    class Meta:
        verbose_name = "Марка техники"
        verbose_name_plural = "Марки техники"

    def __str__(self):
        return self.brand


class MachineryInfo(models.Model):
    mark = models.ForeignKey(
        MachineryBrandname,
        on_delete=models.CASCADE,
        verbose_name="Марка техники",
        related_name="brandname",
        null=True,
    )
    name = models.CharField(
        verbose_name="Модель техники",
        max_length=100,
        blank=False,
        null=False,
    )
    category = models.IntegerField(
        verbose_name="Категория техники",
        choices=Category.choices,
        blank=False,
        null=False,
    )
    description = models.TextField(
        verbose_name="Описание техники",
        blank=False,
        null=False,
    )
    attachments_available = models.BooleanField(
        verbose_name="Возможность навесного оборудования",
        null=False,
    )
    power_hp = models.PositiveSmallIntegerField(
        verbose_name="Мощность, л.с.",
    )
    payload_capacity_kg = models.PositiveSmallIntegerField(
        verbose_name="Грузоподъемность, кг",
    )

    class Meta:
        verbose_name = "Модель техники"
        verbose_name_plural = "Модели техники"

    def __str__(self):
        return f"{self.mark} {self.name}"


class Machinery(models.Model):
    machinery = models.ForeignKey(
        MachineryInfo,
        on_delete=models.PROTECT,
        related_name="machineries",
        verbose_name="Техника",
    )
    year_of_manufacture = models.PositiveSmallIntegerField(
        verbose_name="Год выпуска",
        blank=False,
        null=False,
    )
    available = models.BooleanField(
        verbose_name="Доступность",
        null=False,
        default=True,
    )
    location = models.CharField(
        verbose_name="Местонахождение",
        max_length=100,
        blank=False,
        null=False,
    )
    mileage = models.PositiveSmallIntegerField(
        verbose_name="Пробег",
        blank=False,
        null=False,
    )
    delivery_distance_km = models.PositiveSmallIntegerField(
        verbose_name="Дистанция доставки, км",
        blank=False,
        null=False,
    )
    delivery_cost = models.PositiveIntegerField(
        verbose_name="Стоимость доставки",
        blank=False,
        null=False,
    )
    rental_price = models.PositiveIntegerField(
        verbose_name="Стоимость аренды",
        blank=False,
        null=False,
    )

    class Meta:
        verbose_name = "Карточка техники"
        verbose_name_plural = "Карточки техники"

    def __str__(self):
        return f"{self.machinery.name} - {self.location} ({self.year_of_manufacture})"


class ImageMachinery(models.Model):
    """
    Изображения техники.
    """

    description_image = models.CharField(
        max_length=100,
        blank=True,
    )
    image = models.ImageField(
        upload_to="machinery_image/",
    )
    main_image = models.BooleanField(
        default=False,
    )
    machinery = models.ForeignKey(
        Machinery,
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return f"{self.machinery.machinery.name} {self.description_image}"

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"
        default_related_name = "images_machinery"


class Favorite(models.Model):
    """
    Избранная пользователем техника.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
    )
    machinery = models.ForeignKey(
        Machinery,
        verbose_name="Техника",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные"
        default_related_name = "favorite"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "machinery"],
                name="double favorite (unique)",
            )
        ]

    def __str__(self) -> str:
        return f"{self.user} добавил {self.machinery.machinery.name}"
