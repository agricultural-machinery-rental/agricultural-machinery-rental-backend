import logging

from datetime import datetime
from datetime import timedelta
from datetime import timezone

from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.orders.serializers import (
    CreateReservationSerializer,
    ReadReservationSerializer,
)
from core.choices_classes import ReservationStatusOptions
from machineries.models import Machinery
from orders.models import Reservation
from api.v1.orders.permissions import IsOwner

logger = logging.getLogger(__name__)


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
        logger.info("Запрос на получение списка резервирований")
        return Reservation.objects.filter(renter=self.request.user)

    def get_serializer_class(self):
        if self.action in ("create", "update"):
            return CreateReservationSerializer
        return ReadReservationSerializer

    def perform_create(self, serializer):
        serializer.save(renter=self.request.user)
        machinery = Machinery.objects.get(
            id=self.request.data.get("machinery")
        )
        machinery.count_orders += 1
        machinery.save()

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
        logger.info("Запрос на отмену резервирования")
        reservation = get_object_or_404(Reservation, pk=kwargs["pk"])
        self.check_object_permissions(self.request, reservation)
        current_time = datetime.now(timezone.utc)
        if reservation.status == ReservationStatusOptions.CANCELLED:
            logger.warning("Резерв уже отменен")
            return Response(
                {"message": f"Такой резерв уже отменен!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if reservation.start_date < current_time + timedelta(hours=48):
            logger.warning("Отмена резервации невозможна")
            return Response(
                {
                    "message": f"Отмена невозможна! "
                    f"Осталось менее 48 часов до начала резервации."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        reservation.status = ReservationStatusOptions.CANCELLED
        reservation.save()
        logger.info("Резерв успешно отменен")
        return Response(
            {"message": f"Резерв успешно отменен!"},
            status=status.HTTP_204_NO_CONTENT,
        )
