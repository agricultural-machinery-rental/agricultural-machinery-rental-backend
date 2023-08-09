from rest_framework import mixins, viewsets


from api.v1.orders.serializers import (
    CreateReservationSerializer,
    ReadReservationSerializer,
    ReservationStatusSerializer,
)
from orders.models import Reservation, ReservationStatus
from api.v1.orders.permissions import IsOwner


class ReservationViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """ViewSet для просмотра и обновления резервирований."""

    queryset = Reservation.objects.all()
    serializer_class = CreateReservationSerializer
    # permission_classes = (IsOwner,)

    def get_serializer_class(self):
        if self.request.method in ("POST", "PATCH"):
            return CreateReservationSerializer
        return ReadReservationSerializer


class ReservationStatusViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """ViewSet для просмотра и обновления статусов резервирований."""

    queryset = ReservationStatus.objects.all()
    serializer_class = ReservationStatusSerializer
    # permission_classes = (IsOwner,)
