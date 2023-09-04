from django.contrib import admin

from .models import Location, Region


@admin.register(Region)
class AdminRegion(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)


@admin.register(Location)
class AdminLocation(admin.ModelAdmin):
    list_display = ("title", "region")
    search_fields = ("title", "region__title")
    list_filter = ("region__title",)
