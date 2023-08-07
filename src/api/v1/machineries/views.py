from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from api.v1.machineries.serializers import MachinerySerializer
from machineries.models import Machinery


class MachineryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Вьюсет для техники.
    Обрабатываемые запросы: GET (list&detail).
    Эндпоинты: /machineries/
    Фильтры по Категории (machinery__category), Локации(location),
        Цене(rental_price), Марке техники(machinery__mark),
        Модели техники(machinery__name)
    """

    queryset = Machinery.objects.all()
    serializer_class = MachinerySerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        "machinery__category",
        "location",
        "rental_price",
        "machinery__mark",
        "machinery__name",
    )
