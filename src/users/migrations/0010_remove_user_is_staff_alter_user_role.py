# Generated by Django 4.2.3 on 2023-09-03 17:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0009_user_birthday"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="is_staff",
        ),
        migrations.AlterField(
            model_name="user",
            name="role",
            field=models.IntegerField(
                choices=[(1, "Admin"), (2, "Manager"), (3, "User")],
                default=3,
                verbose_name="Роль",
            ),
        ),
    ]
