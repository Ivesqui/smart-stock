from flask import Blueprint
from web.controllers import alert_controller as controller
from security.decorators import token_required, roles_required

alert_bp = Blueprint("alert", __name__, url_prefix="/alert")

@alert_bp.route("", methods=["GET"])
@token_required
@roles_required("ADMIN", "OPERADOR")
def critical_stock():
    return controller.alerta_stock_critico()

@alert_bp.route("", methods=["GET"])
@token_required
@roles_required("ADMIN", "OPERADOR")
def negative_stock():
    return controller.alerta_stock_negativo()

@alert_bp.route("", methods=["GET"])
@token_required
@roles_required("ADMIN")
def suspicious_movement():
    return controller.alerta_movimiento_sospechoso()

@alert_bp.route("", methods=["GET"])
@token_required
@roles_required("ADMIN", "OPERADOR")
def dead_stock():
    return controller.alerta_stock_muerto()

@alert_bp.route("", methods=["GET"])
@token_required
@roles_required("ADMIN", "OPERADOR")
def stockout_risk():
    return controller.alerta_quiebre_stock()


@alert_bp.route("", methods=["GET"])
@token_required
@roles_required("ADMIN", "OPERADOR")
def overstock():
    return controller.alerta_exceso_stock()



