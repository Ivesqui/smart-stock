from flask import request
from core.entities.product import Product
from utils.responses import success_response, error_response
from container.dependencies import inventario



# Crear producto
def crear_producto():
    try:
        data = request.get_json()
        if not data:
            return error_response("Datos requeridos", 400)
        producto = Product(
            sku=data["sku"],
            codigo_barras=data.get("codigo_barras"),
            nombre_producto=data["nombre_producto"],
            categoria=data["categoria"],
            descripcion=data.get("descripcion"),
            unidad=data["unidad"],
            precio_compra=float(data.get("precio_compra", 0)),
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


# Listar todos los productos activos
def listar_productos():
    estado = request.args.get("estado")  # ACTIVO / INACTIVO
    productos = inventario.listar_productos(estado)
    return success_response(data=productos)


# Buscar producto por SKU
def buscar_por_sku(sku):

    producto = inventario.buscar_por_sku(sku)

    if not producto:
        return error_response("Product no encontrado", 404)

    return success_response(data=producto)


# Buscar producto por nombre
def buscar_por_nombre(nombre):
    productos = inventario.buscar_por_nombre(nombre)
    return success_response(data=productos)


# Buscar producto por código de barras
def buscar_por_codigo(codigo):

    producto = inventario.buscar_por_codigo_barras(codigo)

    if not producto:
        return error_response("Product no encontrado", 404)

    return success_response(data=producto)


# Actualizar producto
def actualizar_producto(sku):
    data = request.get_json()
    actualizado = inventario.actualizar_producto(sku, data)

    if not actualizado:
        return error_response("Product no encontrado", 404)
    return success_response(message="Product actualizado")


# Actualizar productoH parcial
def actualizar_parcial(sku):
    data = request.get_json()
    actualizado = inventario.actualizar_parcial(sku, data)
    if not actualizado:
        return error_response("Product no encontrado", 404)

    return success_response(message="Product actualizado parcialmente")

# Activar producto
def dar_de_alta(sku):
    activado = inventario.activar_producto(sku)
    if not activado:
        return error_response("Product no encontrado", 404)
    return success_response(message="Product activado")

# Desactivar producto
def dar_de_baja(sku):
    eliminado = inventario.desactivar_producto(sku)
    if not eliminado:
        return error_response("Product no encontrado", 404)
    return success_response(message="Product desactivado")
