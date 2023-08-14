from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response


@extend_schema(tags=["Orders"], summary="Тестовая заглушка")
@api_view(["GET"])
def order_hello(request):
    result = {"order": "Hello world"}
    return Response(result)
