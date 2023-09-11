from django.db import models

from locations.managers import LocationManager


class Region(models.Model):
    """Субъект Федерации."""

    title = models.CharField(
        "Наименование", max_length=50, unique=True, db_index=True
    )

    class Meta:
        verbose_name = "Субъект Федерации"
        verbose_name_plural = "Субъекты Федерации"
        ordering = ["title"]

    def __str__(self):
        return self.title


class Location(models.Model):
    """Населенный пункт."""

    title = models.CharField("Наименование", max_length=50)
    region = models.ForeignKey(
        Region,
        on_delete=models.PROTECT,
        verbose_name="Субъект Федерации",
        related_name="locations",
    )

    objects = LocationManager()

    class Meta:
        verbose_name = "Населенный пункт"
        verbose_name_plural = "Населенные пункты"

    def __str__(self):
        return self.title
