from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

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

    @action(
        detail=True,
        methods=("post", "delete"),
        url_path="favorite",
    )
    def favorite(self, request, *args, **kwargs):
        machinery = get_object_or_404(Machinery, pk=kwargs["pk"])
        queryset = Machinery.objects.filter(
            user=request.user, machinery=machinery
        )
        if request.method == "POST":
            if queryset.exists():
                return Response(
                    {
                        "message": f"Такой объект уже добавлен в "
                        f"{Machinery._meta.verbose_name.title()}"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer = MachinerySerializer(
                machinery, context={"request": request}
            )
            Machinery.objects.create(user=request.user, machinery=machinery)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if not queryset:
            return Response(
                {
                    "message": f"Такой объект отсутствует в "
                    f"{Machinery._meta.verbose_name.title()}"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
