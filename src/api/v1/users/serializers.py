from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from core.enums import Limits
from users.models import Callback, User
from api.v1.users.validators import check_names, check_password


class UserSerializer(ModelSerializer):
    role = serializers.CharField(
        source="get_role_display",
        read_only=True,
    )

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "patronymic",
            "phone_number",
            "role",
            "organization_name",
            "inn",
            "birthday",
        )


class CreateUserSerializer(ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    first_name = serializers.CharField(
        max_length=Limits.MAX_LENGTH_FIRST_NAME, validators=[check_names]
    )
    last_name = serializers.CharField(
        max_length=Limits.MAX_LENGTH_LAST_NAME, validators=[check_names]
    )
    patronymic = serializers.CharField(
        max_length=Limits.MAX_LENGTH_PATRONYMIC,
        validators=[check_names],
        allow_blank=True,
        default=None,
    )
    phone_number = PhoneNumberField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    organization_name = serializers.CharField(
        max_length=Limits.MAX_LENGTH_NAME_ORGANIZATION,
        allow_null=True,
        default=None,
    )
    password = serializers.CharField(
        write_only=True, validators=[check_password]
    )

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "patronymic",
            "phone_number",
            "organization_name",
            "inn",
            "birthday",
            "password",
        )

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def validate(self, data):
        if self.context["request"].method != "POST":
            if data.get("password"):
                data.pop("password")
        inn = data.get("inn")
        if inn is None:
            return data
        if not inn.isdigit():
            raise serializers.ValidationError({"inn": "Неверный формат ИНН"})
        return data


class ChangePasswordSerializer(Serializer):
    current_password = serializers.CharField()
    new_password = serializers.CharField()

    def validate(self, attrs):
        user = self.initial_data["user"]
        if not user.check_password(attrs["current_password"]):
            raise serializers.ValidationError({"password": "wrong password"})
        return attrs


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    email_or_phone = serializers.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop("email")
        self.fields["email_or_phone"] = serializers.CharField()

    def get_fields(self):
        fields = super().get_fields()
        fields[self.username_field] = fields.pop("email_or_phone")
        return fields

    def validate(self, attrs):
        email_or_phone = attrs.pop("email_or_phone")
        if "@" in email_or_phone:
            user_data = {"email": email_or_phone}
        else:
            user_data = {"phone_number": email_or_phone}
        user = get_object_or_404(User, **user_data)
        attrs["email"] = user.email
        data = super().validate(attrs)
        return data


class CallbackSerializer(serializers.ModelSerializer):
    """Сериализатор для Обратного звонка."""

    class Meta:
        model = Callback
        fields = (
            "phone_number",
            "comment",
        )


class ResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
