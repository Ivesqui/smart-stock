from flask import Blueprint
from security.decorators import token_required, roles_required
from web.controllers import movement_controller as controller

movement_bp = Blueprint("movements", __name__,url_prefix="/movements")

# MOVIMIENTOS

# registrar movimientos
@movement_bp.route("", methods=["POST"])
@token_required
@roles_required("ADMIN", "OPERADOR")
def register_movement():
    return controller.registrar_movimiento()

# ✔ Ver Kardex
@movement_bp.route("/<string:sku>", methods=["GET"])
@token_required
@roles_required("ADMIN")
def get_movement_by_sku(sku):
    return controller.ver_movimientos(sku)

# PAGINACIÓN

# Listar movimientos
@movement_bp.route("", methods=["GET"])
@token_required
@roles_required("ADMIN", "OPERADOR")
def list_movements():
    return controller.listar_movimientos()

