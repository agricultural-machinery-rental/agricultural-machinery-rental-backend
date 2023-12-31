# Generated by Django 4.2.3 on 2023-08-02 12:17

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0004_callback"),
    ]

    operations = [
        migrations.AlterField(
            model_name="callback",
            name="phone_number",
            field=phonenumber_field.modelfields.PhoneNumberField(
                max_length=15, region=None, verbose_name="Номер телефона"
            ),
        ),
    ]
