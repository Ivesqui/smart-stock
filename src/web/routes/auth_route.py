from flask import Blueprint
from security.decorators import token_required
from web.controllers import auth_controller as controller

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("", methods=["POST"])
def register_route():
    return controller.register()

@auth_bp.route("", methods=["POST"])
def login_route():
    return controller.login()

@auth_bp.route("", methods=["GET"])
@token_required
def me_route():
    return controller.me()