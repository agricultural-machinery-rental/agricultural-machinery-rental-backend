from django.utils import timezone
from django_cron import CronJobBase, Schedule

from core.choices_classes import ReservationStatusOptions
from orders.models import Reservation


class StatusChangingJob(CronJobBase):
    """
    Задача по автоматическому изменению статусов заказов.
    """

    schedule = Schedule(run_every_mins=50, retry_after_failure_mins=5)
    code = "orders.status_changing_job"

    def do(self):
        self.status_changing(
            order_status=ReservationStatusOptions.CREATED,
            new_status=ReservationStatusOptions.CANCELLED,
            field_name="start_date",
        )
        self.status_changing(
            order_status=ReservationStatusOptions.CONFIRMED,
            new_status=ReservationStatusOptions.AT_WORK,
            field_name="start_date",
        )
        self.status_changing(
            order_status=ReservationStatusOptions.AT_WORK,
            new_status=ReservationStatusOptions.FINISHED,
            field_name="end_date",
        )

    def status_changing(
            self,
            order_status: ReservationStatusOptions,
            new_status: ReservationStatusOptions,
            field_name: str,
    ):
        reservations_list = Reservation.objects.filter(
            status=order_status
        )
        if not len(reservations_list) == 0:
            for reserv in reservations_list:
                if getattr(reserv, field_name) < timezone.now():
                    reserv.status = new_status
                    reserv.save()
