from django.urls import path

from api.v1.users.views import user_hello

urlpatterns = [
    path("", user_hello),
]
