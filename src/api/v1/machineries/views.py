from rest_framework import viewsets

from api.v1.machineries.serializers import MachinerySerializer
from machineries.models import Machinery


class MachineryViewSet(viewsets.ModelViewSet):
    queryset = Machinery.objects.all()
    serializer_class = MachinerySerializer
