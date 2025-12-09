import uuid
from datetime import datetime

import bcrypt
from django.db import models


class User(models.Model):
    """Модель пользователя."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def set_password(self, raw_password):
        """Шифровка пароля."""
        self.password_hash = bcrypt.hashpw(raw_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def check_password(self, raw_password):
        """Проверка пароля."""
        return bcrypt.checkpw(raw_password.encode("utf-8"), self.password_hash.encode("utf-8"))

    def __str__(self):
        """Вывод данных по пользователю."""
        return f"{self.first_name} {self.last_name} ({self.email})"



class Role(models.Model):
    """Модель роли."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()

    def __str__(self):
        """Вывод данных по роли."""
        return self.name



class BusinessElement(models.Model):
    """Модель элемента."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()

    def __str__(self):
        """Вывод данных по элементу."""
        return self.name



class AccessRolesRule(models.Model):
    """Правила установки прав доступа."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    element = models.ForeignKey(BusinessElement, on_delete=models.CASCADE)
    read_permission = models.BooleanField(default=False)
    read_all_permission = models.BooleanField(default=False)
    create_permission = models.BooleanField(default=False)
    update_permission = models.BooleanField(default=False)
    update_all_permission = models.BooleanField(default=False)
    delete_permission = models.BooleanField(default=False)
    delete_all_permission = models.BooleanField(default=False)

    class Meta:
        unique_together = ("role", "element")


class Session(models.Model):
    """Модель сессии."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_token = models.CharField(max_length=500, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expire_at = models.DateTimeField()

    def is_valid(self):
        """Валидация сессии."""
        return self.expire_at > datetime.now() and self.user.is_active
