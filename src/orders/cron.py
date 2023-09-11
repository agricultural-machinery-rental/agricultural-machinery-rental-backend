from django.utils import timezone
from django_cron import CronJobBase, Schedule

from core.choices_classes import ReservationStatusOptions
from orders.models import Reservation


class StatusChangingJob(CronJobBase):
    """
    Задача по автоматическому изменению статусов заказов.
    Присваивает заказам статусы 'В работе' и 'Завершен'.
    """

    schedule = Schedule(run_every_mins=50, retry_after_failure_mins=5)
    code = "orders.status_changing_job"

    def do(self):
        created_reservations = Reservation.objects.filter(
            status=ReservationStatusOptions.CREATED
        )
        for reservation in created_reservations:
            if reservation.start_date > timezone.now():
                reservation.status = ReservationStatusOptions.CANCELLED
                reservation.save()

        ongoing_reservations = Reservation.objects.filter(
            status=ReservationStatusOptions.AT_WORK
        )
        for reservation in ongoing_reservations:
            if reservation.end_date > timezone.now():
                reservation.status = ReservationStatusOptions.FINISHED
                reservation.save()

        confirmed_reservations = Reservation.objects.filter(
            status=ReservationStatusOptions.CONFIRMED
        )
        for reservation in confirmed_reservations:
            if reservation.end_date > timezone.now():
                reservation.status = ReservationStatusOptions.FINISHED
                reservation.save()
            if reservation.start_date > timezone.now():
                reservation.status = ReservationStatusOptions.AT_WORK
                reservation.save()
