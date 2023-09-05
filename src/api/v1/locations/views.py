from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, permissions, viewsets

from locations.models import Location, Region

from api.v1.locations.serializers import LocationSerializer, RegionSerializer


@extend_schema(tags=["Region"])
@extend_schema_view(
    list=extend_schema(summary="Список Субъектов Федерации"),
)
class RegionViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Вьюсет для Субъектов Федерации.
    """

    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["title"]


@extend_schema(tags=["Location"])
@extend_schema_view(
    list=extend_schema(summary="Список населенных пунктов"),
)
class LocationViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Вьюсет для населенных пунктов.
    """

    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["title", "region__title"]
