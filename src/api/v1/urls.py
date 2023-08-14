from django.urls import include, path
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView

urlpatterns = [
    path("machineries/", include("api.v1.machineries.urls")),
    path("orders/", include("api.v1.orders.urls")),
    path("users/", include("api.v1.users.urls")),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"
    ),
]
