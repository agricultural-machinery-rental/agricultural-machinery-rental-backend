from rest_framework import serializers

from api.v1.locations.serializers import LocationSerializer
from api.v1.machineries.fields import Base64ImageField, WorkTypeListField
from core.choices_classes import Category

from machineries.models import (
    ImageMachinery,
    Machinery,
    MachineryInfo,
    MachineryBrandname,
    WorkType,
)


class WorkTypeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для видов работ.
    """

    class Meta:
        model = WorkType
        fields = ["title", "slug"]


class MachineryBrandnameSerializer(serializers.ModelSerializer):
    """Сериализация информации о Марке техники"""

    class Meta:
        model = MachineryBrandname
        fields = ("brand", "country_of_origin")


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
    work_type = WorkTypeListField(read_only=True, many=True)

    class Meta:
        fields = (
            "mark",
            "name",
            "category",
            "work_type",
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
    images = ImageSerializer(
        read_only=True,
        many=True,
        source="images_machinery",
    )
    location = LocationSerializer(read_only=True)

    class Meta:
        fields = (
            "id",
            "year_of_manufacture",
            "available",
            "location",
            "mileage",
            "delivery_distance_km",
            "price_per_shift",
            "price_per_hour",
            "is_favorited",
            "machinery",
            "images",
            "count_orders",
        )
        model = Machinery

    def get_is_favorited(self, obj):
        request = self.context.get("request")
        if request.user.is_anonymous:
            return False
        return obj.favorite.filter(user=request.user).exists()
