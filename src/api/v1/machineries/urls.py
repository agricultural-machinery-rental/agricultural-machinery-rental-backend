from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.v1.machineries.views import (
    MachineryViewSet,
    MachineryInfoViewSet,
    MachineryBrandnameViewSet,
    WorkTypeViewSet,
)

v1_router = DefaultRouter()

v1_router.register("machinery", MachineryViewSet, basename="machinery")
v1_router.register("work_type", WorkTypeViewSet, basename="work_type")
v1_router.register("brands", MachineryBrandnameViewSet, basename="brands")
v1_router.register("models", MachineryInfoViewSet, basename="models")

urlpatterns = [
    path("", include(v1_router.urls)),
]
