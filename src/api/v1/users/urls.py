from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from api.v1.users import views

router = DefaultRouter()
router.register("", views.UserViewSet)

urlpatterns = [
    path("change-password/", views.set_password),
    path(
        "password_reset/",
        include("django_rest_passwordreset.urls", namespace="password_reset"),
    ),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("token/", views.MyTokenObtainPairView.as_view()),
    path("callback", views.CallbackList.as_view()),
    path("", include(router.urls)),
]
