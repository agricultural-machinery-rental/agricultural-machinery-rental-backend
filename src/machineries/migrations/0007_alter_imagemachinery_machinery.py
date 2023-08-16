# Generated by Django 4.2.3 on 2023-08-16 13:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        (
            "machineries",
            "0006_machinerybrandname_alter_machineryinfo_options_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="imagemachinery",
            name="machinery",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="machineries.machinery",
            ),
        ),
    ]
