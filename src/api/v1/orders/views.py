from django.shortcuts import get_object_or_404
from rest_framework import status, mixins, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.orders.serializers import (
    CreateReservationSerializer,
    ReservationSerializer,
    ReservationStatusSerializer,
)
from machineries.models import Machinery
from orders.models import Reservation, ReservationStatus


class CreateReservationApiView(APIView):
    """ApiView для создания резервирования."""

    def post(self, request, id):
        machinery = get_object_or_404(Machinery, pk=id)
        data = {
            "renter": request.user.pk,
            "machinery": machinery.pk,
            "start_date": request.data.get("start_date"),
            "end_date": request.data.get("end_date"),
            "comment": request.data.get("comment"),
        }
        serializer = CreateReservationSerializer(
            data=data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class ReservationViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """ViewSet для просмотра и обновления резервирований."""

    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


class ReservationStatusViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """ViewSet для просмотра и обновления статусов резервирований."""

    queryset = ReservationStatus.objects.all()
    serializer_class = ReservationStatusSerializer
