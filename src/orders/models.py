from django.contrib.auth import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404

from core.choices_classes import ReservationStatusOptions
from core.enums import Limits
from machineries.models import Machinery

from .managers import ReservationManagger, ReservationStatusManagger


class Status(models.Model):
    """
    Статус резервирования.
    """

    name = models.IntegerField(
        "Статус резервирования",
        choices=ReservationStatusOptions.choices,
        default=ReservationStatusOptions.CREATED,
    )
    description = models.CharField("Описание статуса", max_length=150)

    class Meta:
        verbose_name = "Статус резервирования"
        verbose_name_plural = "Статусы резервирований"

    def __str__(self):
        return str(self.name)


class Reservation(models.Model):
    """
    Описание модели резервирования техники.
    """

    # ToDo Описать логику формирования номера заказа.
    number = models.CharField("Номер заказа", max_length=30)
    machinery = models.ForeignKey(
        Machinery,
        verbose_name="Техника",
        on_delete=models.CASCADE,
        related_name="reservations",
    )
    renter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Арендатор",
        on_delete=models.CASCADE,
        related_name="reservations",
    )
    start_date = models.DateTimeField(
        "Время начала резервирования",
    )
    end_date = models.DateTimeField(
        "Время окончания резервирования",
    )
    status = models.ManyToManyField(
        Status,
        verbose_name="Статусы резервирования",
        related_name="reservations",
        through="ReservationStatus",
    )
    comment = models.TextField(
        "Комментарий к резервированию",
        max_length=Limits.MAX_LENGTH_COMMENT.value,
        blank=True,
        null=True,
    )

    objects = ReservationManagger

    class Meta:
        verbose_name = "Резервирование"
        verbose_name_plural = "Резервирования"

    def __str__(self):
        return f"{self.machinery} в резерве у {self.renter}"


class ReservationStatus(models.Model):
    """
    Модель для истории изменения статусов заказов.
    """

    status = models.ForeignKey(
        Status,
        on_delete=models.CASCADE,
        verbose_name="Статус заказа",
    )
    reservation = models.ForeignKey(
        Reservation,
        on_delete=models.CASCADE,
        verbose_name="Заказ",
        related_name="reservation_status",
    )
    time_update = models.DateTimeField(
        "Дата изменения статуса",
        auto_now=True,
    )

    objects = ReservationStatusManagger

    class Meta:
        verbose_name = "Статус Заказа"
        verbose_name_plural = "Статусы заказов"

    def __str__(self):
        return f"Заказ {self.reservation}, статус {self.status}"


@receiver(post_save, sender=Reservation)
def create_status(sender, instance, created, **kwargs):
    if created:
        status = get_object_or_404(Status, name=0)
        ReservationStatus.objects.create(status=status, reservation=instance)
