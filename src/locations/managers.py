from django.db import models
from django.db.models.query import QuerySet


class LocationManager(models.Manager):
    """
    Пользовательстки менеджер для модели Субъетов Федерации.
    """
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().select_related("region")
