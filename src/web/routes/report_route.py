from flask import Blueprint
from security.decorators import token_required, roles_required
from web.controllers import report_controller as controller

report_bp = Blueprint("report", __name__, url_prefix="/report")

@report_bp.route("", methods=["GET"])
@token_required # <- autenticación
@roles_required("ADMIN", "OPERADOR")
def inventory_to_report_excel():
    return controller.convertir_inventario_a_excel()

@report_bp.route("", methods=["GET"])
@token_required
@roles_required("ADMIN")
def all_movement_to_report_excel():
    return controller.convertir_movimientos_a_excel()

@report_bp.route("", methods=["GET"])
@token_required
@roles_required("ADMIN")
def all_logs_to_json():
    return controller.convertir_logs_a_json()
