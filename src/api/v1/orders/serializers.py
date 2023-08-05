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
        machinery = validated_data.pop("machinery")
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
