from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import Group

from users.models import User


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
                    "is_active",
                    "role",
                ]
            },
        ),
    ]


admin.site.unregister(Group)
