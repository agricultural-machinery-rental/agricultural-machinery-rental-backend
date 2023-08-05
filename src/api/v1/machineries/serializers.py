from rest_framework import serializers

from core.choices_classes import Category
from machineries.models import Machinery, MachineryInfo


class MachineryInfoSerializer(serializers.ModelSerializer):
    """Сериализация информации о технике."""

    category = serializers.SerializerMethodField()

    class Meta:
        fields = (
            "name",
            "category",
            "description",
            "attachments_available",
            "power_hp",
            "payload_capacity_kg",
        )
        model = MachineryInfo

    def get_category(self, obj):
        return Category(obj.category).label


class MachinerySerializer(serializers.ModelSerializer):
    """Сериализация техники."""

    machinery = MachineryInfoSerializer(read_only=True)

    class Meta:
        fields = (
            "id",
            "year_of_manufacture",
            "available",
            "location",
            "mileage",
            "delivery_distance_km",
            "delivery_cost",
            "rental_price",
            "machinery",
        )
        model = Machinery
