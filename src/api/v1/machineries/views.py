from rest_framework import viewsets

from api.v1.machineries.serializers import MachinerySerializer
from machineries.models import Machinery


class MachineryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Вьюсет для техники.
    Обрабатываемые запросы: GET (list&detail).
    Эндпоинты: /machineries/
    """

    queryset = Machinery.objects.all()
    serializer_class = MachinerySerializer
