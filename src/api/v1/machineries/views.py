from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.machineries.serializers import MachinerySerializer
from api.v1.orders.serializers import CreateReservationSerializer
from machineries.models import Machinery


class MachineryViewSet(viewsets.ModelViewSet):
    queryset = Machinery.objects.all()
    serializer_class = MachinerySerializer

    @action(methods=("POST",), url_path="reserve", detail=True)
    def reserve(self, request, pk):
        user = request.user
        machinery = get_object_or_404(Machinery, pk=pk)
        if request.method == "POST":
            data = {
                "renter": user.pk,
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
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
