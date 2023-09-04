from django.contrib.auth import settings
from django.db import models

from core.choices_classes import Category

from .managers import MachineryManager, MachineryInfoManager


class MachineryBrandname(models.Model):
    """
    Марка техники.
    """

    brand = models.CharField(verbose_name="Марка техники", max_length=100)
    country_of_origin = models.CharField(
        verbose_name="Страна-производитель", max_length=100
    )

    class Meta:
        verbose_name = "Марка техники"
        verbose_name_plural = "Марки техники"
        ordering = ["brand"]

    def __str__(self):
        return self.brand


class MachineryInfo(models.Model):
    """
    Модель техники.
    """

    mark = models.ForeignKey(
        MachineryBrandname,
        on_delete=models.CASCADE,
        verbose_name="Марка техники",
        related_name="brandname",
        null=True,
    )
    name = models.CharField(
        verbose_name="Название",
        max_length=100,
    )
    work_type = models.ManyToManyField(
        "WorkType",
        related_name="machinery_info",
        verbose_name="Тип работ",
    )
    category = models.IntegerField(
        verbose_name="Категория техники",
        choices=Category.choices,
    )
    description = models.TextField(
        verbose_name="Описание техники",
    )
    attachments_available = models.BooleanField(
        verbose_name="Возможность навесного оборудования",
        default=False,
    )
    power_hp = models.PositiveSmallIntegerField(
        verbose_name="Мощность, л.с.",
    )
    payload_capacity_kg = models.PositiveSmallIntegerField(
        verbose_name="Грузоподъемность, кг",
    )

    objects = MachineryInfoManager()

    class Meta:
        verbose_name = "Модель техники"
        verbose_name_plural = "Модели техники"

    def __str__(self):
        return f"{self.mark} {self.name}"


class Machinery(models.Model):
    """
    Каротчка техники.
    """

    machinery = models.ForeignKey(
        MachineryInfo,
        on_delete=models.PROTECT,
        related_name="machineries",
        verbose_name="Техника",
    )
    year_of_manufacture = models.PositiveSmallIntegerField(
        verbose_name="Год выпуска",
    )
    available = models.BooleanField(
        verbose_name="Доступность",
        null=False,
        default=True,
    )
    location = models.CharField(
        verbose_name="Местонахождение",
        max_length=100,
    )
    mileage = models.PositiveSmallIntegerField(
        verbose_name="Пробег",
    )
    delivery_distance_km = models.PositiveSmallIntegerField(
        verbose_name="Дистанция доставки, км",
    )
    price_per_shift = models.DecimalField(
        verbose_name="Цена аренды за смену", max_digits=8, decimal_places=2
    )
    price_per_hour = models.DecimalField(
        verbose_name="Цена аренды в час", max_digits=7, decimal_places=2
    )
    count_orders = models.PositiveIntegerField(
        verbose_name="Количество заказов",
        default=0,
    )

    objects = MachineryManager()

    class Meta:
        verbose_name = "Карточка техники"
        verbose_name_plural = "Карточки техники"

    def __str__(self):
        return (
            f"{self.machinery.name} - {self.location}"
            f" ({self.year_of_manufacture})"
        )


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


class WorkType(models.Model):
    """
    Модель для видов работ.
    """

    title = models.CharField(
        "Название",
        max_length=50,
        unique=True,
    )
    slug = models.SlugField(
        "Слаг",
        max_length=50,
        unique=True,
    )

    class Meta:
        verbose_name = "Вид работ"
        verbose_name_plural = "Виды работ"

    def __str__(self):
        return self.title
