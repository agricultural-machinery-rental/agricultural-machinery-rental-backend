from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.v1.machineries.views import MachineryViewSet

v1_router = DefaultRouter()

v1_router.register("", MachineryViewSet, basename="machinery")

urlpatterns = [
    path("", include(v1_router.urls)),
]
