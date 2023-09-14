from django.contrib.auth import settings
from django.db import models
from django.utils import timezone

from config.settings import PREFIX_ORDER_NUMBER
from core.choices_classes import ReservationStatusOptions
from core.enums import Limits
from machineries.models import Machinery
from orders.managers import ReservationManagger


class Reservation(models.Model):
    """
    Описание модели резервирования техники.
    """

    number = models.CharField(
        verbose_name="Номер заказа",
        max_length=12,
        unique=True,
    )
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

    objects = ReservationManagger()

    class Meta:
        verbose_name = "Резервирование"
        verbose_name_plural = "Резервирования"

    def __str__(self):
        return f"{self.number} | {self.machinery} в резерве у {self.renter}"

    def _generation_number(self) -> str:
        """
        Генерация номера заказа.
        Пример: AG2023000123.
        (AG - префикс, 2023 - год, 000123 - номер).
        """

        prefix: str = PREFIX_ORDER_NUMBER
        number_length: int = Limits.LENGTH_ORDER_NUMBER.value

        year: str = timezone.now().strftime("%Y")
        orders = Reservation.objects.filter(
            number__regex=r"^%s%s[0-9]+" % (prefix, year)
        )

        last_number: int = (
            orders.order_by("-number").values_list("number", flat=True).first()
        )
        last_number: int = (
            int(last_number[len(prefix) + len(year):]) if last_number else 0
        )

        number: int = last_number + 1
        zeros: str = (number_length - len(str(number))) * "0"
        return "{prefix}{year}{number}".format(
            prefix=prefix, year=year, number=zeros + str(number)
        )

    def save(self, *args, **kwargs):
        if not self.number:
            self.number = self._generation_number()
        super(Reservation, self).save(*args, **kwargs)
