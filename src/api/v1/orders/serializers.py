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
        start_date = validated_data["start_date"]
        end_date = validated_data["end_date"]

        if start_date < timezone.now():
            raise serializers.ValidationError("Выбранная дата уже прошла.")

        if end_date < start_date:
            raise serializers.ValidationError(
                "Дата окончания должна быть позже даты начала."
            )

        existing_reservations = Reservation.objects.filter(
            machinery=machinery,
            start_date__lte=end_date,
            end_date__gte=start_date,
        )

        if existing_reservations.exists():
            raise serializers.ValidationError("Выбранные даты уже заняты.")

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


class ReservationSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра и обновления резервирований."""

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

    def update(self, instance, validated_data):
        status_name = validated_data.pop("name")
        status = ReservationStatus.objects.get(name=status_name)
        instance.status = status
        instance.save()
        return instance
