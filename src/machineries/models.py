from django.db import models


class Type(models.Model):
    name = models.CharField(
        verbose_name="Название типа техники",
        unique=True,
        max_length=100,
        blank=False,
        null=False,
    )
    description = models.TextField(
        verbose_name="Описание типа техники",
        blank=False,
        null=False,
    )
    work_type = models.CharField(verbose_name="Предназначение", max_length=150)

    class Meta:
        verbose_name = "Тип техники"
        verbose_name_plural = "Типы техник"

    def __str__(self):
        return self.name


class Machinery(models.Model):
    name = models.CharField(
        verbose_name="Название техники",
        max_length=100,
        blank=False,
        null=False,
    )
    type = models.ForeignKey(
        Type,
        on_delete=models.CASCADE,
        related_name="machineries",
        verbose_name="Тип техники",
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
        verbose_name = "Техника"
        verbose_name_plural = "Техники"

    def __str__(self):
        return self.name


class MachineryList(models.Model):
    machinery = models.ForeignKey(
        Machinery,
        on_delete=models.CASCADE,
        related_name="machineries_list",
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
