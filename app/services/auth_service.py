from core.entities.usuario import Usuario
from security.hash_utils import hash_password, verify_password
from security.jwt_utils import crear_token


class AuthService:

    def __init__(self, usuario_repository):
        self.repo = usuario_repository

    def registrar(self, nombre, email, password, rol="OPERADOR"):

        if self.repo.obtener_por_email(email):
            raise ValueError("El email ya está registrado")

        password_hash = hash_password(password)

        usuario = Usuario(
            nombre=nombre,
            email=email,
            password_hash=password_hash,
            rol=rol
        )

        usuario = self.repo.guardar(usuario)
        print("PASSWORD RECIBIDO:", password)
        print("LENGTH:", len(password))
        print("PASSWORD RECIBIDO:", password)
        print("LENGTH:", len(password))
        return usuario

    def login(self, email, password):

        usuario = self.repo.obtener_por_email(email)

        if not usuario:
            raise ValueError("Credenciales inválidas")

        if not verify_password(password, usuario.password_hash):
            raise ValueError("Credenciales inválidas")

        return crear_token(usuario)