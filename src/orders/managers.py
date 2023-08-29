from typing import Any
from django.db import models


class ReservationManagger(models.Manager):
    """
    Менеджер для модели резервирования техники.
    """

    def get(self, *args: Any, **kwargs: Any) -> Any:
        return (
            super().select_related("machinery", "renter").get(*args, **kwargs)
        )

    def all(self):
        return super().select_related("machinery", "renter").all()


# class ReservationStatusManagger(models.Manager):
#     """
#     Менеджер для модели истории резервирования техники.
#     """
#
#     def get(self, *args: Any, **kwargs: Any) -> Any:
#         return (
#             super()
#             .select_related("status", "reservation")
#             .get(*args, **kwargs)
#         )
#
#     def all(self):
#         return super().select_related("status", "reservation").all()
