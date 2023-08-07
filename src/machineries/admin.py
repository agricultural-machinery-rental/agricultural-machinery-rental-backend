from django.contrib import admin

from machineries.models import (
    Favorite,
    Machinery,
    MachineryInfo,
    MachineryBrandname,
)


@admin.register(Machinery)
class AdminMachinery(admin.ModelAdmin):
    list_display = ("id",)


@admin.register(MachineryInfo)
class AdminMachineryInfo(admin.ModelAdmin):
    list_display = ("id", "name")


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
