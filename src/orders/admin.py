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
    )
    search_fields = (
        "renter__first_name",
        "start_date",
        "end_date",
        "machinary__machinary__name",
    )


@admin.register(ReservationStatus)
class ReservationStatus(admin.ModelAdmin):
    list_display = ("reservation", "status")
    search_fields = ("status__name",)
