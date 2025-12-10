# Система авторизации

Полноценная система аутентификации и авторизации, реализованная с нуля без использования встроенных возможностей
Django/DRF.

---

## Содержание

- Регистрацию, логин, логаут, профиль, мягкое удаление аккаунта
- Систему ролей и гранулярных прав доступа (RBAC)
- JWT токены + сессии с проверкой срока действия
- Middleware для аутентификации каждого запроса
- Swagger документацию API
- Mock бизнес-ресурсы с контролем доступа
- PostgreSQL + bcrypt хэширование паролей

---

## Быстрый запуск (5 минут)

1. Клонирование и установка зависимостей

```
# клонируем проект
git clone https://github.com/kreenna/auth_django
cd auth_django

# создаем виртуальное окружение
python -m venv venv

# активируем окружение
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate     # Windows

# устанавливаем зависимости
pip install -r requirements.txt
```

2. Настройка PostgreSQL

settings.py - обновите параметры БД:

```
python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "auth_system_db",
        "USER": "your_username",
        "PASSWORD": "your_password",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
```

3. Применение миграций и создание суперпользователя

```
# миграции
python manage.py makemigrations
python manage.py migrate

# суперпользователь (для админки)
python manage.py createsuperuser
```

4. запуск сервера

```
# разработка (с авто-перезагрузкой)
python manage.py runserver

# или с Swagger на порту 8000
python manage.py runserver 8000
```

Сервер доступен по адресу: http://localhost:8000

---

### Swagger документация API

Swagger автоматически генерируется с помощью drf-spectacular и доступен по адресу:

🔗 http://localhost:8000/docs/

Что показывает Swagger:

- Полную интерактивную документацию всех endpoints
- Примеры запросов и ответов
- Поля для ввода токенов (Authorization: Bearer YOUR_TOKEN)
- Авто-тестирование API прямо в браузере

---

### Система прав доступа (RBAC)

Роли по умолчанию:

- ```admin``` - полный доступ
- ```manager``` - чтение/создание/обновление всех
- ```user``` - чтение/создание своих объектов

---

### Безопасность

- Пароли: bcrypt с salt (12 раундов)
- Токены: JWT с 24ч lifetime
- Сессии: проверка expire_at + is_active
- Middleware: проверка каждого запроса
- Ошибки: 401 (не авторизован), 403 (нет прав)
- CORS: настроен для разработки

---

# Линтеры

```
pip install black flake8
black .
flake8 .
```

---
