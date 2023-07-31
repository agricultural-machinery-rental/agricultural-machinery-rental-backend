from django.contrib import admin

from orders.models import Reservation, ReservationStatus


@admin.register(Reservation)
class AdminReservation(admin.ModelAdmin):
    list_display = (
        "id",
        "machinery",
        "renter",
        "start_date",
        "end_date",
        "status",
        "is_need_attachment",
        "is_need_driver",
        "is_need_delivery",
    )


@admin.register(ReservationStatus)
class AdminReservationStatus(admin.ModelAdmin):
    list_display = (
        "name",
        "time_update",
    )
