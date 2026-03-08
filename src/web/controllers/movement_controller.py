from flask import request, g
from container.dependencies import inventario
from utils.responses import success_response, error_response



# MOVIMIENTOS


# Registrar movimiento
def registrar_movimiento():

    try:
        data = request.get_json()
        if not data:
            return error_response("Body requerido", 400)

        required_fields = ["sku", "tipo", "cantidad"]

        for field in required_fields:
            if field not in data:
                return error_response(f"Campo requerido: {field}", 400)

        user = g.user
        resultado = inventario.registrar_movimiento(
            sku=data["sku"],
            tipo=data["tipo"],
            cantidad=int(data["cantidad"]),
            motivo=data.get("motivo", ""),
            usuario_id=user["user_id"]
        )

        if not resultado:
            return error_response("Product no encontrado", 404)

        return success_response(message="Movimiento registrado")

    except ValueError as e:
        return error_response(str(e), 400)

    except Exception:
        return error_response("Error interno del servidor", 500)


# Kardex
def ver_movimientos(sku):
    movimientos = inventario.obtener_movimientos_por_sku(sku)
    return success_response(data=movimientos)


# PAGINACIÓN

def listar_movimientos():

    filtros = {
        "sku": request.args.get("sku"),
        "tipo": request.args.get("tipo"),
        "usuario_id": request.args.get("usuario_id"),
        "fecha_desde": request.args.get("fecha_desde"),
        "fecha_hasta": request.args.get("fecha_hasta"),
    }

    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
    except ValueError:
        return error_response("page y limit deben ser números", 400)

    resultado = inventario.listar_movimientos(filtros, page, limit)

    return success_response(data=resultado)



