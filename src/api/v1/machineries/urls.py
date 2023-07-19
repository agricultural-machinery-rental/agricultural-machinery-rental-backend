from django.urls import path

from api.v1.machineries.views import machineries_hello

urlpatterns = [
    path("", machineries_hello),
]
