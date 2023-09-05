from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework import mixins, viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
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
        Цене аренды в час(price_per_hour), за смену(price_per_shift),
        Марке техники(machinery__mark), Модели техники(machinery__name),
        Видам работ (machinery__work_type)
    """

    queryset = Machinery.objects.filter(available=True)
    serializer_class = MachinerySerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MachineryFilter
    pagination_class = LimitOffsetPagination

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

    @extend_schema(summary="Получить топ заказываемых машин", methods=["GET"])
    @action(
        detail=False,
        methods=("get",),
        url_path="top",
        permission_classes=(AllowAny,),
    )
    def top(self, request):
        paginator = LimitOffsetPagination()
        queryset = Machinery.objects.order_by("-count_orders")
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = MachinerySerializer(
            result_page, many=True, context={"request": request}
        )
        return paginator.get_paginated_response(serializer.data)

    @extend_schema(
        summary="Получить список техники в избранном", methods=["GET"]
    )
    @action(
        detail=False,
        methods=("get",),
        url_path="favorites",
        permission_classes=(permissions.IsAuthenticated,),
    )
    def favorites(self, request):
        current_user = request.user
        paginator = LimitOffsetPagination()
        queryset = Machinery.objects.filter(favorite__user=current_user)
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = MachinerySerializer(
            result_page, many=True, context={"request": request}
        )
        return paginator.get_paginated_response(serializer.data)


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
