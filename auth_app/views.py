from datetime import datetime, timedelta

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, Session
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserSerializer
from .services import create_jwt_token


class RegisterView(APIView):
    """Регистрация."""
    permission_classes = [AllowAny]

    def post(self, request):
        """Обработка POST запросов."""
        serializer = UserRegisterSerializer(data=request.data)
        # проверяем корректность пароля
        if serializer.is_valid():
            user = serializer.save()
            token = create_jwt_token(user.id)
            session = Session.objects.create(
                user=user,
                session_token=token,
                expire_at=datetime.now() + timedelta(hours=24)
            )
            return Response({
                "message": "Пользователь зарегистрирован",
                "token": token,
                "user": UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """Авторизация."""
    permission_classes = [AllowAny]

    def post(self, request):
        """Обработка POST запросов."""
        serializer = UserLoginSerializer(data=request.data)
        # проверяем корректность пароля
        if serializer.is_valid():
            user = User.objects.filter(email=serializer.validated_data["email"], is_active=True).first()
            if user and user.check_password(serializer.validated_data["password"]):
                token = create_jwt_token(user.id)
                Session.objects.create(
                    user=user,
                    session_token=token,
                    expire_at=datetime.now() + timedelta(hours=24)
                )
                return Response({
                    "message": "Успешный вход",
                    "token": token,
                    "user": UserSerializer(user).data
                })
            return Response({"error": "Неверные данные"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """Выход из аккаунта."""

    def post(self, request):
        """Обработка POST запросов."""
        token = request.META.get("HTTP_AUTHORIZATION", "").replace("Bearer ", "")
        Session.objects.filter(session_token=token).delete()
        return Response({"message": "Выход выполнен"}, status=status.HTTP_200_OK)
