from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.v1.locations.views import LocationViewSet, RegionViewSet

location_router = DefaultRouter()

location_router.register("regions", RegionViewSet, "regions")
location_router.register("locations", LocationViewSet, "locations")

urlpatterns = [
    path("", include(location_router.urls)),
]
