from django.urls import path

from .views import CallbackList


urlpatterns = [
    path("callback", CallbackList.as_view()),
]
