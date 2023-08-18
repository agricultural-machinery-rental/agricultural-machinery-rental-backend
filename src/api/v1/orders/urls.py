from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.v1.orders.views import ReservationViewSet

v1_router = DefaultRouter()

v1_router.register("", ReservationViewSet, basename="orders")

urlpatterns = [
    path("", include(v1_router.urls)),
]
