from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework import mixins, viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from api.v1.machineries.serializers import (
    MachinerySerializer,
    MachineryBrandnameSerializer,
    MachineryInfoSerializer,
    WorkTypeSerializer,
)
from api.v1.machineries.filters import MachineryFilter
from machineries.models import (
    Favorite,
    Machinery,
    MachineryInfo,
    MachineryBrandname,
    WorkType,
)


@extend_schema(tags=["Machinery"])
@extend_schema_view(
    list=extend_schema(summary="Список техники"),
    retrieve=extend_schema(summary="Конкретная техника"),
)
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
    filterset_class = MachineryFilter

    @extend_schema(summary="Отметить как избранное", methods=["POST"])
    @extend_schema(summary="Исключить из избранного", methods=["DELETE"])
    @action(
        detail=True,
        methods=("post", "delete"),
        url_path="favorite",
        permission_classes=(permissions.IsAuthenticated,),
    )
    def favorite(self, request, *args, **kwargs):
        machinery = get_object_or_404(Machinery, pk=kwargs["pk"])
        queryset = Favorite.objects.filter(
            user=request.user, machinery=machinery
        )
        if request.method == "POST":
            if queryset.exists():
                return Response(
                    {
                        "message": f"Такой объект уже добавлен в "
                        f"{Favorite._meta.verbose_name.title()}"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer = MachinerySerializer(
                machinery, context={"request": request}
            )
            Favorite.objects.create(user=request.user, machinery=machinery)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if not queryset:
            return Response(
                {
                    "message": f"Такой объект отсутствует в "
                    f"{Favorite._meta.verbose_name.title()}"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["WorkType"])
@extend_schema_view(
    list=extend_schema(summary="Список видов работ"),
)
class WorkTypeViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = WorkTypeSerializer
    queryset = WorkType.objects.all()
    permission_classes = [
        permissions.AllowAny,
    ]


@extend_schema(tags=["MachineryBrandname"])
@extend_schema_view(
    list=extend_schema(summary="Список марок техники"),
)
class MachineryBrandnameViewSet(
    mixins.ListModelMixin, viewsets.GenericViewSet
):
    serializer_class = MachineryBrandnameSerializer
    queryset = MachineryBrandname.objects.all()
    permission_classes = [
        permissions.AllowAny,
    ]


@extend_schema(tags=["MachineryInfo"])
@extend_schema_view(
    list=extend_schema(summary="Список моделей техники"),
)
class MachineryInfoViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = MachineryInfoSerializer
    queryset = MachineryInfo.objects.all()
    permission_classes = [
        permissions.AllowAny,
    ]
