from django.db import models


class ReservationManagger(models.Manager):
    """
    Менеджер для модели резервирования техники.
    """

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related(
                "renter",
                "machinery",
                "machinery__machinery",
                "machinery__location",
            )
        )
