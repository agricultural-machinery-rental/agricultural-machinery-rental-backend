from django.contrib import admin

from orders.models import Order, Reservation, ReservationList


@admin.register(Order)
class AdminOrder(admin.ModelAdmin):
    list_display = (
        "id",
        "reservation_list",
        "payment_status",
        "date_from",
        "date_to",
    )


@admin.register(Reservation)
class AdminReservation(admin.ModelAdmin):
    list_display = ("id",)


@admin.register(ReservationList)
class AdminReservationList(admin.ModelAdmin):
    list_display = ("id",)
