from django.db.models import Q
from rest_framework import serializers

from api.v1.orders import validators
from api.v1.users.serializers import UserSerializer
from core.choices_classes import ReservationStatusOptions
from machineries.models import Machinery
from orders.models import Reservation


class CreateReservationSerializer(serializers.ModelSerializer):
    """Сериализатор для создания резервирования."""

    machinery = serializers.PrimaryKeyRelatedField(
        queryset=Machinery.objects.all(),
    )
    start_date = serializers.DateTimeField(
        validators=[validators.validate_start_date]
    )

    class Meta:
        fields = (
            "machinery",
            "start_date",
            "end_date",
            "comment",
        )
        model = Reservation
        validators = [validators.validate_end_date]

    def validate(self, data):
        existing_reservations = Reservation.objects.filter(
            machinery=data.get("machinery"),
            start_date__lte=data.get("end_date"),
            end_date__gte=data.get("start_date"),
        ).exclude(
            Q(status=ReservationStatusOptions.CANCELLED)
            | Q(status=ReservationStatusOptions.FINISHED)
        )
        if self.context["request"].method == "PUT":
            instance_id = (
                self.context["request"].parser_context.get("kwargs").get("pk")
            )
            existing_reservations = existing_reservations.exclude(
                id=instance_id
            )
        if existing_reservations.exists():
            raise serializers.ValidationError("Выбранные даты уже заняты.")
        return data

    def create(self, validated_data):
        machinery = validated_data["machinery"]
        self.validate(validated_data)
        reservation = Reservation.objects.create(
            machinery_id=machinery.id, **validated_data
        )
        return reservation

    def update(self, instance, validated_data):
        self.validate(validated_data)
        instance = super().update(instance, validated_data)
        return instance

    def to_representation(self, instance):
        return ReadReservationSerializer(
            instance, context={"request": self.context.get("request")}
        ).data


class ReadReservationSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра резервирований."""

    renter = UserSerializer(read_only=True)

    class Meta:
        model = Reservation
        fields = (
            "id",
            "number",
            "machinery",
            "renter",
            "start_date",
            "end_date",
            "status",
            "comment",
            "cost",
        )
