from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.orders.serializers import CreateReservationSerializer
from machineries.models import Machinery


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
