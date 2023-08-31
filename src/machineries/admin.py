from django.contrib import admin

from machineries.models import (
    Favorite,
    Machinery,
    MachineryInfo,
    MachineryBrandname,
    ImageMachinery,
    WorkType,
)


@admin.register(Machinery)
class AdminMachinery(admin.ModelAdmin):
    list_display = (
        "id",
        "machinery",
        "year_of_manufacture",
        "location",
        "available",
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


@admin.register(MachineryBrandname)
class AdminMachineryBrandname(admin.ModelAdmin):
    list_display = ("id", "brand")


@admin.register(WorkType)
class AdminWorkType(admin.ModelAdmin):
    list_display = ("slug", "title")
