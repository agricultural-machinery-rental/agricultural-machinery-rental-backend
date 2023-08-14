from django.contrib import admin

from machineries.models import (
    Favorite,
    Machinery,
    MachineryInfo,
    ImageMachinery,
)


@admin.register(Machinery)
class AdminMachinery(admin.ModelAdmin):
    list_display = (
        "id",
        "machinery",
        "year_of_manufacture",
        "available",
        "location",
    )


@admin.register(MachineryInfo)
class AdminMachineryInfo(admin.ModelAdmin):
    list_display = ("id", "name", "category", "description")


@admin.register(ImageMachinery)
class AdminImageMachinery(admin.ModelAdmin):
    list_display = (
        "id",
        "machinery",
        "description_image",
        "image",
        "main_image",
    )


@admin.register(Favorite)
class FavoriteInfo(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "machinery",
    )
