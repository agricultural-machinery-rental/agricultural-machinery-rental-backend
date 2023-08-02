from django.contrib import admin

from machineries.models import Machinery, MachineryInfo


@admin.register(Machinery)
class AdminMachinery(admin.ModelAdmin):
    list_display = ("id",)


@admin.register(MachineryInfo)
class AdminMachineryInfo(admin.ModelAdmin):
    list_display = ("id",)
