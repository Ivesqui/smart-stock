from flask import Blueprint
from security.decorators import token_required, roles_required
from web.controllers import user_controller as controller

user_bp = Blueprint("user", __name__, url_prefix="/user")

# Listar todos los usuarios
@user_bp.route("", methods=["GET"])
@token_required
@roles_required("ADMIN")
def get_all_users():
    return controller.listar_usuarios()

# Obtener usuario por id
@user_bp.route("/<int:user_id>", methods=["GET"])
@token_required
@roles_required("ADMIN")
def get_users_by_id(user_id):
    return controller.obtener_usuario(user_id)

# Cambiar rol de usuario
@user_bp.route("/<int:user_id>/role", methods=["PATCH"])
@token_required
@roles_required("ADMIN")
def change_rol(user_id):
    return controller.cambiar_rol(user_id)

# Desactivar usuario
@user_bp.route("/<int:user_id>/deactivate", methods=["PATCH"])
@token_required
@roles_required("ADMIN")
def deactivate_user(user_id):
    return controller.desactivar_usuario(user_id)

# Activar usuario
@user_bp.route("/<int:user_id>/activate", methods=["PATCH"])
@token_required
@roles_required("ADMIN")
def activate_user(user_id):
    return controller.activar_usuario(user_id)

# Obtener logs de auditoria
@user_bp.route("/audit-logs", methods=["GET"])
@token_required
@roles_required("ADMIN")
def get_audit_logs():
    return controller.obtener_audit_logs()