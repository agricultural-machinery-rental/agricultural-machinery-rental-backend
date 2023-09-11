from django.db import models
from django.db.models.query import QuerySet


class MachineryInfoManager(models.Manager):
    """
    Пользовательсткий менеджер для модели "Модель техники".
    """

    def get_queryset(self) -> QuerySet:
        return (
            super()
            .get_queryset()
            .select_related("mark")
            .prefetch_related("work_type")
        )


class MachineryManager(models.Manager):
    """
    Пользовательсткий менеджер для модели "Каротчка техники".
    """

    def get_queryset(self) -> QuerySet:
        return (
            super()
            .get_queryset()
            .select_related(
                "machinery", "machinery__mark", "location", "location__region"
            )
            .prefetch_related("machinery__work_type", "images_machinery")
        )
