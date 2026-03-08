from flask import Blueprint
from security.decorators import token_required, roles_required
from web.controllers import product_controller as controller

product_bp = Blueprint("products", __name__, url_prefix="/products")

# Crear producto
@product_bp.route("", methods=["POST"])
@token_required
@roles_required("ADMIN", "OPERADOR")
def create_product():
    return controller.crear_producto()

# Listar todos / activos
@product_bp.route("", methods=["GET"])
@token_required
@roles_required("ADMIN", "OPERADOR")
def list_products():
    return controller.listar_productos()

# Buscar por SKU
@product_bp.route("/<sku>", methods=["GET"])
@token_required
@roles_required("ADMIN", "OPERADOR")
def get_by_sku(sku):
    return controller.buscar_por_sku(sku)

# Buscar por nombre
@product_bp.route("/<nombre>", methods=["GET"])
@token_required
@roles_required("ADMIN", "OPERADOR")
def get_by_name(nombre):
    return controller.buscar_por_nombre(nombre)

# Buscar por código de barras
@product_bp.route("/barcode/<codigo>", methods=["GET"])
@token_required
#@roles_required("ADMIN", "OPERADOR")
def get_by_barcode(codigo):
    return controller.buscar_por_codigo(codigo)

# Actualizar producto
@product_bp.route("/<sku>", methods=["PUT"])
@token_required
@roles_required("ADMIN", "OPERADOR")
def update_total(sku):
    return controller.actualizar_producto(sku)

# Actualizar parcial
@product_bp.route("/<sku>", methods=["PATCH"])
@token_required
@roles_required("ADMIN", "OPERADOR")
def update_partial(sku):
    return controller.actualizar_parcial(sku)

# Activar producto
@product_bp.route("/<sku>/enable", methods=["PATCH"])
@token_required
@roles_required("ADMIN", "OPERADOR")
def enable_product(sku):
    return controller.dar_de_alta(sku)

# Desactivar producto
@product_bp.route("/<sku>/disable", methods=["PATCH"])
@token_required
@roles_required("ADMIN", "OPERADOR")
def disable_product(sku):
    return controller.dar_de_baja(sku)