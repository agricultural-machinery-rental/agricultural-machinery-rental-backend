from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from users.models import User


@admin.register(User)
class MyAdmin(UserAdmin):
    search_fields = ("email", "first_name")
    list_display = ("username", "first_name", "email")


admin.site.unregister(Group)
