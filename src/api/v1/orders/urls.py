from django.urls import path

from api.v1.orders.views import order_hello

urlpatterns = [
    path("", order_hello),
]
