from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from core.enums import Limits
from users.models import User


class AuthTokenSerializer(ModelSerializer):
    password = serializers.CharField(
        write_only=True,
    )

    class Meta:
        model = User
        fields = ("email", "password")

    def validate(self, attrs):
        user = get_object_or_404(User, email=attrs["email"])
        if not user.check_password(attrs["password"]):
            raise serializers.ValidationError({"password": "wrong password"})
        return attrs


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "patronymic",
            "phone_number",
            "role",
        )


class CreateUserSerializer(ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    first_name = serializers.CharField(
        max_length=Limits.MAX_LENGTH_FIRST_NAME,
    )
    last_name = serializers.CharField(max_length=Limits.MAX_LENGTH_LAST_NAME)
    patronymic = serializers.CharField(
        max_length=Limits.MAX_LENGTH_PATRONYMIC, allow_blank=True, default=None
    )
    phone_number = PhoneNumberField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "patronymic",
            "phone_number",
            "password",
        )

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class ChangePasswordSerializer(Serializer):
    current_password = serializers.CharField()
    new_password = serializers.CharField()

    def validate(self, attrs):
        user = self.initial_data["user"]
        if not user.check_password(attrs["current_password"]):
            raise serializers.ValidationError({"password": "wrong password"})
        return attrs


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        return data
