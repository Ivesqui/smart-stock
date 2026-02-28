

class UserService:

    def __init__(self, user_repository):
        self.repo = user_repository

    # ================================
    # CONSULTAS
    # ================================

    def listar_usuarios(self):
        return self.repo.listar_usuarios()

    def obtener_por_id(self, user_id):
        usuario = self.repo.obtener_por_id(user_id)
        if not usuario:
            raise ValueError("Usuario no encontrado")
        return usuario

    # ================================
    # ADMINISTRACIÓN
    # ================================

    def cambiar_rol(self, user_id, nuevo_rol, current_user):

        usuario = self.repo.obtener_por_id(user_id)
        rol_anterior = usuario.rol
        if not usuario:
            raise ValueError("Usuario no encontrado")

        # No permitir cambiarse su propio rol
        if usuario.id == current_user["user_id"]:
            raise ValueError("No puedes cambiar tu propio rol")

        roles_validos = ["ADMIN", "OPERADOR"]

        if nuevo_rol not in roles_validos:
            raise ValueError("Rol inválido")

        # Si el usuario es el último ADMIN activo, no permitir degradarlo
        if usuario.rol == "ADMIN" and nuevo_rol != "ADMIN":
            admins_activos = self.repo.contar_admins_activos()
            if admins_activos <= 1:
                raise ValueError("No se puede remover el último ADMIN")

        self.repo.actualizar_rol(user_id, nuevo_rol)

        self.audit_service.log(
            user_id=current_user["user_id"],
            action="CHANGE_ROLE",
            target_user_id=user_id,
            details=f"{rol_anterior} → {nuevo_rol}")

    def desactivar_usuario(self, user_id, current_user):

        usuario = self.repo.obtener_por_id(user_id)
        if not usuario:
            raise ValueError("Usuario no encontrado")

        # No permitir desactivarse a sí mismo
        if usuario.id == current_user["user_id"]:
            raise ValueError("No puedes desactivarte a ti mismo")

        # No permitir desactivar último ADMIN
        if usuario.rol == "ADMIN":
            admins_activos = self.repo.contar_admins_activos()
            if admins_activos <= 1:
                raise ValueError("No se puede desactivar el último ADMIN")

        self.repo.actualizar_estado(user_id, False)
        self.audit_service.log(
            user_id=current_user["user_id"],
            action="DEACTIVATE_USER",
            target_user_id=user_id
        )

    def activar_usuario(self, user_id):

        usuario = self.repo.obtener_por_id(user_id)
        if not usuario:
            raise ValueError("Usuario no encontrado")

        self.repo.actualizar_estado(user_id, True)