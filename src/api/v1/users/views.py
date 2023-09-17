import logging

from django.contrib.auth import get_user_model
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiExample,
)
from rest_framework import generics, mixins, permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from api.v1.users import serializers
from api.v1.users.permissions import OwnerOrAdminPermission, OwnerPermission
from users.models import Callback

User = get_user_model()

logger = logging.getLogger(__name__)


class NotListViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pass


@extend_schema(tags=["Users"])
@extend_schema_view(
    create=extend_schema(
        summary="Создание нового пользователя",
        examples=[
            OpenApiExample(
                "Пример создания пользователя",
                value={
                    "email": "user@example.com",
                    "first_name": "Иван",
                    "last_name": "Иванов",
                    "phone_number": "+79451234567",
                    "password": "superPuper",
                },
                status_codes=[str(status.HTTP_201_CREATED)],
            ),
        ],
    ),
    retrieve=extend_schema(summary="Конкретный пользователь"),
    update=extend_schema(summary="Изменение данных пользователя"),
    partial_update=extend_schema(
        summary="Изменение данных пользователя",
        examples=[
            OpenApiExample(
                "Пример изменения данных пользователя",
                value={
                    "first_name": "Пётр",
                    "last_name": "Иванов",
                    "organization_name": "AMR",
                    "inn": "123456789112",
                },
                status_codes=[str(status.HTTP_200_OK)],
            ),
        ],
    ),
    destroy=extend_schema(summary="Удаление пользователя"),
)
class UserViewSet(NotListViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action in ["create", "partial_update"]:
            return serializers.CreateUserSerializer
        return serializers.UserSerializer

    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAny()]
        return [OwnerOrAdminPermission()]


@extend_schema(
    tags=["Users"],
    summary="Получить токен пользователя",
    description=(
        "Получить токен пользователя можно указав почту или номер "
        "телефона и пароль"
    ),
    examples=[
        OpenApiExample(
            "Пример получения токена",
            value={
                "email_or_phone": "user@example.com",
                "password": "superPuper",
            },
            status_codes=[str(status.HTTP_200_OK)],
        ),
    ],
)
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.CustomTokenObtainPairSerializer


@extend_schema(
    tags=["Users"],
    summary="Изменить пароль пользователя",
    request=serializers.ChangePasswordSerializer,
    examples=[
        OpenApiExample(
            "Пример изменения пароля пользователя",
            value={
                "current_password": "superPuper",
                "new_password": "superPuper2",
            },
            status_codes=[str(status.HTTP_204_NO_CONTENT)],
        ),
    ],
)
@api_view(["POST"])
@permission_classes([OwnerPermission])
def set_password(request):
    data = request.data
    data["user"] = request.user
    serializer = serializers.ChangePasswordSerializer(data=data)
    if serializer.is_valid():
        user = request.user
        user.set_password(request.data["new_password"])
        user.save()
        logger.info("Пароль успешно изменен")
        return Response(status=status.HTTP_204_NO_CONTENT)
    logger.warning(
        f"Пользователь: {request.user.email} ,"
        f"Метод запроса: {request.method} ,"
        f"Неверные данные для изменения пароля - {serializer.errors}"
    )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Callback"], summary="Обратный звонок")
class CallbackList(generics.CreateAPIView):
    """
    Дженерик для Обратного звонка.
    Обрабатывает только POST запрос.
    Доступен неавторизованным пользователям.
    Эндпоинт users/callback.
    """

    queryset = Callback.objects.all()
    serializer_class = serializers.CallbackSerializer
    permission_classes = [permissions.AllowAny]
