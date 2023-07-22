from datetime import timedelta

from django.contrib.auth import settings
from django.db import models

from core.choices_classes import OrderStatus, ReservationStatus
from core.enums import Limits
from machineries.models import MachineryInfo


class Reservation(models.Model):
    """
    Описание модели резервирования техники.
    """

    machinery = models.ForeignKey(
        MachineryInfo,
        verbose_name="Техника",
        on_delete=models.CASCADE,
        related_name="reservations",
    )
    renter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Арендодатель",
        on_delete=models.CASCADE,
        related_name="reservation_renters",
    )
    tenant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Арендатор",
        on_delete=models.CASCADE,
        related_name="reservation_tenants",
    )
    reservation_status = models.IntegerField(
        "Статус резервирования",
        choices=ReservationStatus.choices,
        blank=True,
        null=True,
    )
    date_from = models.DateTimeField(
        "Дата создания резервирования",
        auto_now_add=True,
    )
    date_to = models.DateTimeField(
        "Дата окончания срока резервирования",
    )

    class Meta:
        verbose_name = ("Резервирование",)
        verbose_name_plural = "Резервирования"
        ordering = ("date_from",)

    def __str__(self):
        return f"{self.machinery} в резерве у {self.tenant}"

    def save(self, *args, **kwargs):
        if self.date_from and not self.date_to:
            self.date_to = self.date_from + timedelta(days=1)
        super().save(*args, **kwargs)


class ReservationList(models.Model):
    """
    Список техники в резерве.
    """

    reservation = models.ManyToManyField(
        Reservation,
        verbose_name="Резервирование",
        related_name="reservation_lists",
    )
    quantity = models.PositiveSmallIntegerField(
        "Количество единиц",
        default=Limits.DEFAULT_QUANTITY,
    )

    class Meta:
        verbose_name = "Список резервов"
        verbose_name_plural = "Списки резервирований"


class Order(models.Model):
    """
    Описание модели заказа.
    """

    reservation_list = models.OneToOneField(
        ReservationList,
        verbose_name="Резервирование",
        on_delete=models.CASCADE,
        related_name="orders",
    )
    payment_status = models.BooleanField(
        "Статус оплаты",
        default=False,
    )
    order_status = models.IntegerField(
        "Статус заказа",
        choices=OrderStatus.choices,
        blank=True,
        null=True,
    )
    date_from = models.DateTimeField(
        "Дата создания заказа",
        auto_now_add=True,
    )
    date_to = models.DateTimeField(
        "Дата исполнения заказа",
        auto_now=True,
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ("date_from",)

    def __str__(self):
        return f"Заказ на {self.reservation_list}"
