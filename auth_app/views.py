from datetime import datetime, timedelta

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, Session
from .permissions import HasPermission
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


class UserProfileView(APIView):
    """Отображение профиля."""

    def get(self, request):
        """Обработка GET запросов."""
        return Response(UserSerializer(request.user).data)

    def patch(self, request):
        """Обработка PATCH запросов."""
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        # проверяем корректность пароля
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteAccountView(APIView):
    """Удаление аккаунта."""

    def post(self, request):
        """Обработка POST запросов."""
        request.user.is_active = False
        request.user.save()
        # выход из аккаунта
        token = request.META.get("HTTP_AUTHORIZATION", "").replace("Bearer ", "")
        Session.objects.filter(session_token=token).delete()
        return Response({"message": "Аккаунт удален"}, status=status.HTTP_200_OK)


# Mock бизнес-ресурсы
class ProductsView(APIView):
    permission_classes = [IsAuthenticated, HasPermission]
    element_name = "products"

    def get(self, request):
        """Обработка GET запросов."""
        return Response({"products": [
            {"id": 1, "name": "Product 1", "owner": request.user.id},
            {"id": 2, "name": "Product 2", "owner": request.user.id}
        ]})

    def post(self, request):
        """Обработка POST запросов."""
        return Response({"message": "Продукт создан", "id": 3})


class OrdersView(APIView):
    """Отображение заказов."""
    permission_classes = [IsAuthenticated, HasPermission]
    element_name = "orders"

    def get(self, request):
        """Обработка GET запросов."""
        return Response({"orders": [
            {"id": 1, "product": "Product 1", "status": "pending"},
            {"id": 2, "product": "Product 2", "status": "completed"}
        ]})
