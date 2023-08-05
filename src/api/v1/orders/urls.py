from django.urls import path

from api.v1.orders.views import CreateReservationApiView

app_name = "orders"

urlpatterns = [
    path(
        "machineries/<int:id>/reserve/",
        CreateReservationApiView.as_view(),
        name="create_reservation",
    ),
]
