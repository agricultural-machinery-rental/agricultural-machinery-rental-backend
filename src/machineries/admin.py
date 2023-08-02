from django.contrib import admin

from machineries.models import Favorite, Machinery, MachineryInfo


@admin.register(Machinery)
class AdminMachinery(admin.ModelAdmin):
    list_display = ("id",)


@admin.register(MachineryInfo)
class AdminMachineryInfo(admin.ModelAdmin):
    list_display = ("id",)


@admin.register(Favorite)
class FavoriteInfo(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "machinery",
    )
