from django.contrib.auth import settings
from django.db import models

from core.choices_classes import ReservationStatusOptions
from core.enums import Limits
from machineries.models import Machinery


class ReservationStatus(models.Model):
    """
    Статус резервирования.
    """

    name = models.IntegerField(
        "Статус резервирования",
        choices=ReservationStatusOptions.choices,
        default=ReservationStatusOptions.CREATED,
    )
    time_update = models.DateTimeField(
        "Дата изменения статуса",
        auto_now=True,
    )

    class Meta:
        verbose_name = "Статус резервирования"
        verbose_name_plural = "Статусы резервирований"


class Reservation(models.Model):
    """
    Описание модели резервирования техники.
    """

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
        "Дата начала резервирования",
    )
    end_date = models.DateTimeField(
        "Дата окончания резервирования",
    )
    status = models.OneToOneField(
        ReservationStatus,
        verbose_name="Статус резервирования",
        on_delete=models.PROTECT,
        related_name="reservations",
    )
    is_need_attachment = models.BooleanField(
        "Навесное оборудование",
        default=False,
    )
    is_need_driver = models.BooleanField(
        "Водитель техники",
        default=False,
    )
    is_need_delivery = models.BooleanField(
        "Доставка техники",
        default=False,
    )
    comment = models.TextField(
        "Комментарий к резервированию",
        max_length=Limits.RESERVATION_COMMENT_MAX_LENGTH,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = ("Резервирование",)
        verbose_name_plural = "Резервирования"

    def __str__(self):
        return f"{self.machinery} в резерве у {self.renter}"
