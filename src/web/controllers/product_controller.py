from flask import request, g
from web.app import auth_service, user_service
from utils.responses import success_response, error_response
from security.decorators import token_required


# ======================================================
# PRODUCTOS
# ======================================================

# ✔ Crear product
#@app.route("/productos", methods=["POST"])
@token_required
#@roles_required("ADMIN", "OPERADOR")
def crear_producto():
    try:
        data = request.get_json()

        producto = Product(
            sku=data["sku"],
            codigo_barras=data.get("codigo_barras"),
            nombre_producto=data["nombre_producto"],
            categoria=data["categoria"],
            descripcion=data.get("descripcion"),
            unidad=data["unidad"],
            precio_compra=float(data["precio_compra"]),
            precio_venta=float(data["precio_venta"]),
            stock_actual=int(data["stock_actual"]),
            stock_minimo=int(data["stock_minimo"]),
            activo=True
        )

        inventario.crear_producto(producto)

        return success_response(message="Product creado", status=201)

    except ValueError as e:
        return error_response(str(e), 400)

    except Exception:
        return error_response("Error interno del servidor", 500)


# ✔ Listar todos / activos
#@app.route("/productos", methods=["GET"])
@token_required
#@roles_required("ADMIN", "OPERADOR")
def listar_productos():

    estado = request.args.get("estado")  # ACTIVO / INACTIVO

    productos = inventario.listar_productos(estado)

    return success_response(data=productos)


# ✔ Buscar por SKU
#@app.route("/productos/<sku>", methods=["GET"])
@token_required
#@roles_required("ADMIN", "OPERADOR")
def buscar_por_sku(sku):

    producto = inventario.buscar_por_sku(sku)

    if not producto:
        return error_response("Product no encontrado", 404)

    return success_response(data=producto)


# ✔ Buscar por nombre
#@app.route("/productos/nombre/<nombre>", methods=["GET"])
@token_required
#@roles_required("ADMIN", "OPERADOR")
def buscar_por_nombre(nombre):

    productos = inventario.buscar_por_nombre(nombre)

    return success_response(data=productos)


# ✔ Buscar por código de barras
#@app.route("/productos/barcode/<codigo>", methods=["GET"])
@token_required
#@roles_required("ADMIN", "OPERADOR")
def buscar_por_codigo(codigo):

    producto = inventario.buscar_por_codigo_barras(codigo)

    if not producto:
        return error_response("Product no encontrado", 404)

    return success_response(data=producto)


# ✔ PUT total
#@app.route("/productos/<sku>", methods=["PUT"])
@token_required
#@roles_required("ADMIN", "OPERADOR")
def actualizar_total(sku):

    data = request.get_json()

    actualizado = inventario.actualizar_producto(sku, data)

    if not actualizado:
        return error_response("Product no encontrado", 404)

    return success_response(message="Product actualizado")


# ✔ PATCH parcial
#@app.route("/productos/<sku>", methods=["PATCH"])
@token_required
#@roles_required("ADMIN", "OPERADOR")
def actualizar_parcial(sku):

    data = request.get_json()

    actualizado = inventario.actualizar_parcial(sku, data)

    if not actualizado:
        return error_response("Product no encontrado", 404)

    return success_response(message="Product actualizado parcialmente")

# ✔ PATCH alta lógica
#@app.route("/productos/<sku>/alta", methods=["PATCH"])
@token_required
#@roles_required("ADMIN", "OPERADOR")
def dar_de_alta(sku):

    activado = inventario.activar_producto(sku)

    if not activado:
        return error_response("Product no encontrado", 404)

    return success_response(message="Product activado")

# ✔ PATCH baja lógica
#@app.route("/productos/<sku>/baja", methods=["PATCH"])
@token_required
#@roles_required("ADMIN", "OPERADOR")
def dar_de_baja(sku):

    eliminado = inventario.desactivar_producto(sku)

    if not eliminado:
        return error_response("Product no encontrado", 404)

    return success_response(message="Product desactivado")
