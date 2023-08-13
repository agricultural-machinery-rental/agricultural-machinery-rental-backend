from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def order_hello(request):
    result = {"order": "Hello world"}
    return Response(result)
