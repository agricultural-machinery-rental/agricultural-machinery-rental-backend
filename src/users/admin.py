from django.contrib import admin
from django.contrib.admin import ModelAdmin
from rest_framework.authtoken.admin import TokenProxy

from users.models import Callback, User


@admin.register(User)
class UserAdmin(ModelAdmin):
    ordering = ["email"]
    search_fields = ("email", "last_name", "first_name")
    list_display = (
        "email",
        "last_name",
        "first_name",
        "patronymic",
        "phone_number",
        "is_active",
        "role",
        "date_joined",
    )

    fieldsets = [
        (
            "Main",
            {
                "fields": [
                    "email",
                    "last_name",
                    "first_name",
                    "patronymic",
                    "phone_number",
                    "birthday",
                    "organization_name",
                    "inn",
                    "is_active",
                    "role",
                    "groups",
                ]
            },
        ),
    ]


@admin.register(Callback)
class CallbackAdmin(ModelAdmin):
    search_fields = ("phone_number",)
    list_display = (
        "phone_number",
        "comment",
        "is_finished",
        "time_create",
        "time_finished",
    )


admin.site.unregister(TokenProxy)
