from django.contrib import admin

from orders.models import Reservation


@admin.register(Reservation)
class AdminReservation(admin.ModelAdmin):
    list_display = (
        "id",
        "machinery",
        "renter",
        "start_date",
        "end_date",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "renter__first_name",
        "start_date",
        "end_date",
        "machinary__machinary__name",
        "created_at",
        "updated_at",
    )
