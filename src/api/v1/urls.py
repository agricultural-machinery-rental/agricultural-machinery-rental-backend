from django.urls import include, path

urlpatterns = [
    path("machineries/", include("api.v1.machineries.urls")),
    # path("orders/", include("api.v1.orders.urls")),
    path("users/", include("api.v1.users.urls")),
]
