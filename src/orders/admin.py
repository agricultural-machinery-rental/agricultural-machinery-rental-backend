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
    )


@admin.register(ReservationStatus)
class AdminReservationStatus(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "time_update",
    )
