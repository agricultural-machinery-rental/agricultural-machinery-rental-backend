from rest_framework import serializers

from orders.models import Machinery


class MachinerySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id",)
        model = Machinery
