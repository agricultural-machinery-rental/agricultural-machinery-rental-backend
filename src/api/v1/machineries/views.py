from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def machineries_hello(request):
    result = {"machinery": "Hello world"}
    return Response(result)
