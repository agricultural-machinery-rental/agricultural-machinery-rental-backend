from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from api.v1.users import serializers
from api.v1.users.permissions import NicePerson

User = get_user_model()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return serializers.CreateUserSerializer
        return serializers.UserSerializer

    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAny()]
        return [NicePerson()]


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.CustomTokenObtainPairSerializer


@api_view(["POST"])
@permission_classes([NicePerson])
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
