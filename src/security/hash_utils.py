from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["argon2", "bcrypt"],
    deprecated="auto"
)

def hash_password(password: str) -> str:
    if not password:
        raise ValueError("La contraseña no puede estar vacía")
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    try:
        return pwd_context.verify(password, hashed)
    except Exception:
        return False