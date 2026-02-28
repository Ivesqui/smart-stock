import sqlite3
from core.entities.user import User


class SqliteUserRepository:

    def __init__(self, db_path):
        self.db_path = db_path

    def _conectar(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    # ======================================================
    # CREAR USUARIO
    # ======================================================
    def guardar(self, usuario: User):

        conn = self._conectar()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO usuarios (
                nombre,
                email,
                password_hash,
                rol,
                activo,
                fecha_creacion
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            usuario.nombre,
            usuario.email,
            usuario.password_hash,
            usuario.rol,
            1 if usuario.activo else 0,
            usuario.to_dict()["fecha_creacion"]
        ))

        conn.commit()

        usuario._Usuario__id = cursor.lastrowid
        conn.close()

        return usuario

    # ======================================================
    # OBTENER POR EMAIL
    # ======================================================
    def obtener_por_email(self, email: str):

        conn = self._conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM usuarios WHERE email = ?
        """, (email,))

        row = cursor.fetchone()
        conn.close()

        if not row:
            return None

        return self._row_to_usuario(row)

    # ======================================================
    # OBTENER POR ID
    # ======================================================
    def obtener_por_id(self, user_id: int):

        conn = self._conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM usuarios WHERE id = ?
        """, (user_id,))

        row = cursor.fetchone()
        conn.close()

        if not row:
            return None

        return self._row_to_usuario(row)

    # ======================================================
    # LISTAR USUARIOS
    # ======================================================
    def listar_usuarios(self):

        conn = self._conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM usuarios")
        rows = cursor.fetchall()
        conn.close()

        return [self._row_to_usuario(row) for row in rows]

    # ======================================================
    # ACTUALIZAR PASSWORDS
    # ======================================================

    def actualizar_password(self, user_id: int, nuevo_hash: str):

        conn = self._conectar()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE usuarios
            SET password_hash = ?
            WHERE id = ?
        """, (nuevo_hash, user_id))

        conn.commit()
        conn.close()


    # ======================================================
    # ACTUALIZAR ESTADO
    # ======================================================
    
    def actualizar_estado(self, user_id: int, activo: int):

        conn = self._conectar()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE usuarios
            SET activo = ?
            WHERE id = ?
        """, (activo, user_id))

        conn.commit()
        conn.close()


    # ======================================================
    # CONTAR ADMINS ACTIVOS
    # ======================================================


    def contar_admins_activos(self):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute = """
            SELECT COUNT(*) 
            FROM users 
            WHERE rol = 'ADMIN' AND activo = 1
        """
        conn.commit()
        conn.close()

    # ======================================================
    # CONVERTIR FILA A OBJETO
    # ======================================================
    def _row_to_usuario(self, row):

        return User(
            user_id=row["id"],
            nombre=row["nombre"],
            email=row["email"],
            password_hash=row["password_hash"],
            rol=row["rol"],
            activo=bool(row["activo"]),
            fecha_creacion=row["fecha_creacion"]
        )

