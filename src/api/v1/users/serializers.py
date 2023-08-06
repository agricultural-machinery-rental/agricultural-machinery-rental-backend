from rest_framework import serializers

from users.models import Callback


class CallbackSerializer(serializers.ModelSerializer):
    """Сериализатор для Обратного звонка."""

    class Meta:
        model = Callback
        fields = (
            "phone_number",
            "comment",
        )
