from datetime import datetime
from datetime import timedelta
from datetime import timezone

from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, viewsets
from rest_framework import status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from api.v1.orders.serializers import (
    CreateReservationSerializer,
    ReadReservationSerializer,
)
from core.choices_classes import ReservationStatusOptions
from orders.models import Reservation
from api.v1.orders.permissions import IsOwner


@extend_schema(tags=["Orders"])
@extend_schema_view(
    list=extend_schema(summary="Список резерваций"),
    retrieve=extend_schema(summary="Конкретный резерв"),
)
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
        if self.action in ("create", "update"):
            return CreateReservationSerializer
        return ReadReservationSerializer

    def perform_create(self, serializer):
        serializer.save(renter=self.request.user)

    def perform_update(self, serializer):
        serializer.save(renter=self.request.user)

    @extend_schema(
        summary="Отменить резервацию",
        methods=["POST"],
        request=None,
        responses={
            status.HTTP_204_NO_CONTENT: "Резерв успешно отменен!",
        },
    )
    @action(
        detail=True,
        methods=("post",),
        url_path="cancel",
        permission_classes=(IsOwner,),
    )
    def cancel(self, request, *args, **kwargs):
        """
        Отмена резервирования пользователем.
        """
        reservation = get_object_or_404(Reservation, pk=kwargs["pk"])
        self.check_object_permissions(self.request, reservation)
        current_time = datetime.now(timezone.utc)
        if reservation.status == ReservationStatusOptions.CANCELLED:
            return Response(
                {"message": f"Такой резерв уже отменен!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if reservation.start_date < current_time + timedelta(hours=48):
            return Response(
                {
                    "message": f"Отмена невозможна! "
                    f"Осталось менее 48 часов до начала резервации."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        reservation.status = ReservationStatusOptions.CANCELLED
        reservation.save()
        return Response(
            {"message": f"Резерв успешно отменен!"},
            status=status.HTTP_204_NO_CONTENT,
        )


@extend_schema(tags=["Orders"], summary="Тестовая заглушка")
@api_view(["GET"])
def order_hello(request):
    result = {"order": "Hello world"}
    return Response(result)
