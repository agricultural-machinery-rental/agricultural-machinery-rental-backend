from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers

from api.v1.users.serializers import UserSerializer
from core.choices_classes import ReservationStatusOptions
from machineries.models import Machinery
from orders.models import Reservation, ReservationStatus


class ReservationStatusSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра и изменения статусов резервирования."""

    class Meta:
        fields = ("id", "name", "time_update")
        model = ReservationStatus


class CreateReservationSerializer(serializers.ModelSerializer):
    """Сериализатор для создания резервирования."""

    machinery = serializers.PrimaryKeyRelatedField(
        queryset=Machinery.objects.all(),
    )
    renter = UserSerializer(read_only=True)

    class Meta:
        fields = (
            "id",
            "machinery",
            "renter",
            "start_date",
            "end_date",
            "comment",
        )
        model = Reservation

    def create(self, validated_data):
        current_user = self.context["request"].user
        machinery = validated_data["machinery"]
        self.validate(validated_data)

        status = ReservationStatus.objects.create(
            name=ReservationStatusOptions.CREATED
        )
        reservation = Reservation.objects.create(
            machinery_id=machinery.id,
            renter=current_user,
            status=status,
            **validated_data
        )
        return reservation

    def update(self, instance, validated_data):
        self.validate(validated_data)
        instance = super().update(instance, validated_data)
        return instance

    def validate(self, data):

        if data.get("start_date") < timezone.now():
            raise serializers.ValidationError("Выбранная дата уже прошла.")
        if data.get("end_date") < data.get("start_date"):
            raise serializers.ValidationError(
                "Дата окончания должна быть позже даты начала."
            )
        existing_reservations = Reservation.objects.filter(
            machinery=data.get("machinery"),
            start_date__lte=data.get("end_date"),
            end_date__gte=data.get("start_date"),
        ).exclude(status__name=ReservationStatusOptions.CANCELLED)

        if existing_reservations.exists():
            raise serializers.ValidationError("Выбранные даты уже заняты.")

        return data


class ReadReservationSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра резервирований."""

    status = ReservationStatusSerializer()

    class Meta:
        fields = (
            "id",
            "machinery",
            "renter",
            "start_date",
            "end_date",
            "status",
        )
        model = Reservation
