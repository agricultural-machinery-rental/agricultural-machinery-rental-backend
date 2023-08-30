from django.contrib.auth import settings
from django.db import models

from core.choices_classes import ReservationStatusOptions
from core.enums import Limits
from machineries.models import Machinery

from orders.managers import ReservationManagger


class Reservation(models.Model):
    """
    Описание модели резервирования техники.
    """

    number = models.CharField("Номер заказа", max_length=30, default=1)
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
        null=True,
    )
    start_date = models.DateTimeField(
        "Время начала резервирования",
        null=True,
    )
    end_date = models.DateTimeField(
        "Время окончания резервирования",
        null=True,
    )
    status = models.IntegerField(
        verbose_name="Статусы резервирования",
        choices=ReservationStatusOptions.choices,
        default=ReservationStatusOptions.CREATED,
    )
    comment = models.TextField(
        "Комментарий к резервированию",
        max_length=Limits.MAX_LENGTH_COMMENT.value,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True,
        blank=True,
        null=True,
    )
    updated_at = models.DateTimeField(
        verbose_name="Дата обновления",
        auto_now=True,
        blank=True,
        null=True,
    )

    objects = ReservationManagger

    class Meta:
        verbose_name = "Резервирование"
        verbose_name_plural = "Резервирования"

    def __str__(self):
        return f"{self.machinery} в резерве у {self.renter}"
