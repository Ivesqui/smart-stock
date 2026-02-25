import jwt
from datetime import datetime, timedelta
import os


SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

def crear_token(usuario):
    payload = {
        "user_id": usuario.id,
        "email": usuario.email,
        "rol": usuario.rol,
        "exp": datetime.utcnow() + timedelta(hours=8)
    }

    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verificar_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])