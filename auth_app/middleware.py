import jwt
from django.http import JsonResponse
from rest_framework import status

from .models import Session


class AuthMiddleware:
    """Middleware сервиса."""

    def __init__(self, get_response):
        """Инициализация."""
        self.get_response = get_response

    def __call__(self, request):
        """Обработка вызова."""
        # получаем токен из заголовка
        auth_header = request.META.get("HTTP_AUTHORIZATION", "")
        if auth_header.startswith("Bearer "):
            token = auth_header[7:]
            try:
                # проверяем сессию
                session = Session.objects.filter(session_token=token).first()
                if session and session.is_valid():
                    request.user = session.user
                else:
                    return JsonResponse({"error": "Недействительный токен"}, status=status.HTTP_401_UNAUTHORIZED)
            except jwt.ExpiredSignatureError:
                return JsonResponse({"error": "Токен истек"}, status=status.HTTP_401_UNAUTHORIZED)
            except jwt.InvalidTokenError:
                return JsonResponse({"error": "Недействительный токен"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            request.user = None

        response = self.get_response(request)
        return response
