from datetime import datetime, timedelta

import jwt


def create_jwt_token(user_id):
    """Создание JWT токена."""
    payload = {
        "user_id": str(user_id),
        "exp": datetime.now() + timedelta(hours=24),
        "iat": datetime.now()
    }
    return jwt.encode(payload, "secret-key", algorithm="HS256")
