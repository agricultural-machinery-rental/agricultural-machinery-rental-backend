# Generated by Django 4.2.3 on 2023-08-18 08:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Status",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.IntegerField(
                        choices=[
                            (0, "Created"),
                            (1, "Confirmed"),
                            (2, "Cancelled"),
                            (3, "At Work"),
                            (4, "Finished"),
                        ],
                        default=0,
                        verbose_name="Статус резервирования",
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        max_length=150, verbose_name="Описание статуса"
                    ),
                ),
            ],
            options={
                "verbose_name": "Статус резервирования",
                "verbose_name_plural": "Статусы резервирований",
            },
        ),
        migrations.AlterModelOptions(
            name="reservation",
            options={
                "verbose_name": "Резервирование",
                "verbose_name_plural": "Резервирования",
            },
        ),
        migrations.AlterModelOptions(
            name="reservationstatus",
            options={
                "verbose_name": "Статус Заказа",
                "verbose_name_plural": "Статусы заказов",
            },
        ),
        migrations.RemoveField(
            model_name="reservationstatus",
            name="name",
        ),
        migrations.AddField(
            model_name="reservation",
            name="number",
            field=models.CharField(
                default=1, max_length=30, verbose_name="Номер заказа"
            ),
        ),
        migrations.AddField(
            model_name="reservation",
            name="renter",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="reservations",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Арендатор",
            ),
        ),
        migrations.AddField(
            model_name="reservationstatus",
            name="reservation",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="reservation_status",
                to="orders.reservation",
                verbose_name="Заказ",
            ),
        ),
        migrations.AlterField(
            model_name="reservation",
            name="end_date",
            field=models.DateTimeField(
                null=True, verbose_name="Время окончания резервирования"
            ),
        ),
        migrations.AlterField(
            model_name="reservation",
            name="start_date",
            field=models.DateTimeField(
                null=True, verbose_name="Время начала резервирования"
            ),
        ),
        migrations.AddField(
            model_name="reservation",
            name="status",
            field=models.ManyToManyField(
                related_name="reservations",
                through="orders.ReservationStatus",
                to="orders.status",
                verbose_name="Статусы резервирования",
            ),
        ),
        migrations.AddField(
            model_name="reservationstatus",
            name="status",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="orders.status",
                verbose_name="Статус заказа",
            ),
        ),
    ]
