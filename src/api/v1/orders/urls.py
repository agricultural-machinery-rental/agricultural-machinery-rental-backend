from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.v1.orders.views import (
    CreateReservationApiView,
    ReservationStatusViewSet,
    ReservationViewSet,
)

app_name = "orders"

v1_router = DefaultRouter()

v1_router.register("reservations", ReservationViewSet, basename="reservation")
v1_router.register(
    "reservations_statuses",
    ReservationStatusViewSet,
    basename="reservation_statuses",
)

urlpatterns = [
    path(
        "machineries/<int:id>/reserve/",
        CreateReservationApiView.as_view(),
        name="create_reservation",
    ),
    path("", include(v1_router.urls)),
]
