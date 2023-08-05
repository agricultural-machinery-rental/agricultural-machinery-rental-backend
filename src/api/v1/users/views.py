from rest_framework import generics
from rest_framework.permissions import AllowAny

from users.models import Callback
from api.v1.users.serializers import CallbackSerializer


class CallbackList(generics.CreateAPIView):
    queryset = Callback.objects.all()
    serializer_class = CallbackSerializer
    permission_classes = [AllowAny]
