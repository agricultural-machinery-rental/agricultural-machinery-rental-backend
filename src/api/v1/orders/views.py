from rest_framework import mixins, viewsets


from api.v1.orders.serializers import (
    CreateReservationSerializer,
    ReadReservationSerializer,
)
from orders.models import Reservation
from api.v1.orders.permissions import IsOwner


class ReservationViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """ViewSet для просмотра и обновления резервирований."""

    permission_classes = (IsOwner,)

    def get_queryset(self):
        return Reservation.objects.filter(renter=self.request.user)

    def get_serializer_class(self):
        if self.request.method in ("POST", "PATCH"):
            return CreateReservationSerializer
        return ReadReservationSerializer

    def perform_create(self, serializer):
        serializer.save(renter=self.request.user)
