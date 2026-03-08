from flask import Blueprint
from security.decorators import token_required, roles_required
from web.controllers import dashboard_controller as controller

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@dashboard_bp.route("/dashboard/resumen", methods=["GET"])
@token_required
@roles_required("ADMIN")
def resume():
    return controller.dashboard()