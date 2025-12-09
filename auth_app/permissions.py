from rest_framework.permissions import BasePermission

from .models import AccessRolesRule, Role, BusinessElement


class HasPermission(BasePermission):
    """Проверка прав доступа."""
    def has_permission(self, request, view):
        """Метод для осуществления проверки прав доступа."""
        if not request.user:
            return False

        # получаем роль пользователя (пока простая логика, можно расширить)
        user_role = Role.objects.filter(name="user").first()  # По умолчанию user

        element_name = getattr(view, "element_name", "unknown")
        action = request.method.lower()

        # маппинг HTTP методов на разрешения
        permission_map = {
            "get": "read_permission" if "list" in request.path else "read_all_permission",
            "post": "create_permission",
            "patch": "update_permission",
            "put": "update_all_permission",
            "delete": "delete_permission",
        }

        # проверяем наличие прав доступа
        permission_field = permission_map.get(action)
        if not permission_field:
            return False

        # проверяем работоспособность прав доступа
        try:
            element = BusinessElement.objects.get(name=element_name)
            rule = AccessRolesRule.objects.get(role=user_role, element=element)
            return getattr(rule, permission_field)
        except:
            return False
