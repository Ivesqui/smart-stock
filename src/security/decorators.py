from functools import wraps
from flask import request
from security.jwt_utils import verificar_token
from flask import g
import jwt

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return {"error": "Token requerido"}, 401

        if not auth_header.startswith("Bearer "):
            return {"error": "Formato de token inválido"}, 401

        try:
            token = auth_header.split(" ")[1]
            decoded = verificar_token(token)
            g.user = decoded

        except jwt.ExpiredSignatureError:
            return {"error": "Token expirado"}, 401

        except jwt.InvalidTokenError:
            return {"error": "Token inválido"}, 401

        except Exception:
            return {"error": "Error de autenticación"}, 401

        return f(*args, **kwargs)

    return decorated

def roles_required(*roles):
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):

            user = getattr(request, "user", None)

            if not user:
                return {"error": "User no autenticado"}, 401

            if user.get("rol") not in roles:
                return {"error": "No autorizado"}, 403

            return f(*args, **kwargs)

        return decorated
    return wrapper