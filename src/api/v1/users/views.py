from django.contrib.auth import get_user_model
from rest_framework import generics, mixins, permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from api.v1.users import serializers
from api.v1.users.permissions import OwnerOrAdminPermission, OwnerPermission
from users.models import Callback

User = get_user_model()


class NotListViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pass


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


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.CustomTokenObtainPairSerializer


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
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
