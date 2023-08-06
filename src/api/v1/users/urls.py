from django.urls import path

from api.v1.users.views import CallbackList


urlpatterns = [
    path("callback", CallbackList.as_view()),
]
