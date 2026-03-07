from security.decorators import token_required
from utils.responses import success_response

# ======================================================
# GESTIÓN DE USUARIOS
# ======================================================

#ADMIN

# Listar todos los usuarios
#@app.route("/users", methods=["GET"])
@token_required
#@roles_required("ADMIN")
def listar_usuarios():

    usuarios = user_service.listar_usuarios()
    return success_response(data=[u.to_dict() for u in usuarios])

# Obtener usuario por id
#@app.route("/users/<int:user_id>", methods=["GET"])
@token_required
#@roles_required("ADMIN")
def obtener_usuario(user_id):

    usuario = user_service.obtener_por_id(user_id)
    return success_response(data=usuario.to_dict())

# Cambiar rol de usuario
#@app.route("/users/<int:user_id>/role", methods=["PATCH"])
@token_required
#@roles_required("ADMIN")
def cambiar_rol(user_id):

    data = request.get_json()
    current_user = g.user

    user_service.cambiar_rol(
        user_id,
        data["rol"],
        current_user
    )

    return success_response(message="Rol actualizado")

# Desactivar usuario
#@app.route("/users/<int:user_id>/deactivate", methods=["PATCH"])
@token_required
#@roles_required("ADMIN")
def desactivar_usuario(user_id):

    current_user = g.user
    user_service.desactivar_usuario(user_id, current_user)

    return success_response(message="Usuario desactivado")

# Activar usuario
#@app.route("/users/<int:user_id>/activate", methods=["PATCH"])
@token_required
#@roles_required("ADMIN")
def activar_usuario(user_id):

    user_service.activar_usuario(user_id)

    return success_response(message="Usuario activado")

# Obtener logs de auditoria

#@app.route("/admin/audit-logs", methods=["GET"])
@token_required
#@roles_required("ADMIN")
def obtener_audit_logs():

    logs = audit_serv.obtener_logs()
    return success_response(data=logs)