from datetime import datetime


class Usuario:

    def __init__(
        self,
        nombre: str,
        email: str,
        password_hash: str,
        rol: str = "OPERADOR",
        activo: bool = True,
        fecha_creacion: str = None,
        user_id: int = None

    ):
        self.__id = user_id
        self.__nombre = nombre
        self.__email = email
        self.__password_hash = password_hash
        self.__rol = rol
        self.__activo = activo
        self.__fecha_creacion = fecha_creacion or datetime.now().isoformat()
        if not email or not nombre:
            raise ValueError("Nombre y email son obligatorios")

    def to_dict(self):
        return {
            "id": self.__id,
            "nombre": self.__nombre,
            "email": self.__email,
            "rol": self.__rol,
            "activo": self.__activo,
            "fecha_creacion": self.__fecha_creacion
        }



    @property
    def id(self): return self.__id
    @property
    def nombre(self): return self.__nombre
    @property
    def email(self): return self.__email
    @property
    def password_hash(self): return self.__password_hash
    @property
    def rol(self): return self.__rol
    @property
    def activo(self): return self.__activo