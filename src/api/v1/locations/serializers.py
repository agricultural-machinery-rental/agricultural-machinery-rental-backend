from rest_framework import serializers

from locations.models import Location, Region


class RegionSerializer(serializers.ModelSerializer):
    """
    Сериализатор для Субъектов Федерации.
    """

    class Meta:
        model = Region
        fields = ("id", "title")


class LocationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для населенных пунктов.
    """

    region = serializers.StringRelatedField()

    class Meta:
        model = Location
        fields = ("id", "title", "region")
