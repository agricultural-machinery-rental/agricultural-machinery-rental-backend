from rest_framework import serializers

from api.v1.machineries.fields import Base64ImageField
from core.choices_classes import Category

from machineries.models import (
    ImageMachinery,
    Machinery,
    MachineryInfo,
    MachineryBrandname,
)


class MachineryBrandnameSerializer(serializers.ModelSerializer):
    """Сериализация информации о Марке техники"""

    class Meta:
        model = MachineryBrandname
        fields = ("brand",)


class ImageSerializer(serializers.ModelSerializer):
    """Сериализация изображений."""

    image = Base64ImageField(
        required=True,
    )

    class Meta:
        fields = (
            "id",
            "image",
            "main_image",
            "description_image",
        )
        model = ImageMachinery


class MachineryInfoSerializer(serializers.ModelSerializer):
    """Сериализация информации о технике."""

    category = serializers.SerializerMethodField()
    mark = MachineryBrandnameSerializer(read_only=True)
    images = ImageSerializer(
        read_only=True,
        many=True,
        source="images_machinery",
    )

    class Meta:
        fields = (
            "mark",
            "name",
            "images",
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
    is_favorited = serializers.SerializerMethodField(read_only=True)

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
            "is_favorited",
            "machinery",
        )
        model = Machinery

    def get_is_favorited(self, obj):
        request = self.context.get("request")
        if request.user.is_anonymous:
            return False
        return obj.favorite.filter(user=request.user).exists()
