from django.utils import timezone
from rest_framework import serializers


def validate_start_date(start_date):
    if start_date < timezone.now():
        raise serializers.ValidationError("Выбранная дата уже прошла.")


def validate_end_date(data):
    if data.get("end_date") < data.get("start_date"):
        raise serializers.ValidationError(
            "Дата окончания должна быть позже даты начала."
        )
