from rest_framework import generics

from users.models import Callback
from .serializers import CallbackSerializer


class CallbackList(generics.ListCreateAPIView):
    queryset = Callback.objects.all()
    serializer_class = CallbackSerializer
