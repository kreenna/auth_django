from rest_framework import serializers

from .models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации пользователя."""
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "middle_name", "email", "password", "password_confirm"]

    def validate(self, attrs):
        """Валидация пароля."""
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError("Пароли не совпадают")
        return attrs

    def create(self, validated_data):
        """Установка пароля."""
        validated_data.pop("password_confirm")
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    """Сериализатор авторизации пользователя."""
    email = serializers.EmailField()
    password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя."""
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "middle_name", "email", "is_active"]
        read_only_fields = ["id"]
