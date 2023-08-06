from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.v1.users import views

router = DefaultRouter()
router.register("", views.UserViewSet)

urlpatterns = [
    path("change-password/", views.set_password),
    path("logout/", views.del_token),
    path("token/", views.MyTokenObtainPairView.as_view()),
    path("", include(router.urls)),
]
