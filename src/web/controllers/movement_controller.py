import os
from flask import request, g
from services.inventory_service import InventoryService
from security.decorators import token_required
from utils.responses import success_response

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "inventario.db")
repo = SqliteProductRepository(DB_PATH)
inventario = InventoryService(repo)


# MOVIMIENTOS
# ======================================================

# ✔ Registrar movimiento
@app.route("/movimientos", methods=["POST"])
@token_required
@roles_required("ADMIN", "OPERADOR")
def registrar_movimiento():

    try:
        data = request.get_json()

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


# ✔ Ver Kardex
@app.route("/productos/<sku>/movimientos", methods=["GET"])
@token_required
@roles_required("ADMIN")
def ver_movimientos(sku):

    movimientos = inventario.obtener_movimientos_por_sku(sku)

    return success_response(data=movimientos)

# ======================================================
# PAGINACIÓN
# ======================================================
#@app.route("/movimientos", methods=["GET"])
@token_required
#@roles_required("ADMIN", "OPERADOR")
def listar_movimientos():

    filtros = {
        "sku": request.args.get("sku"),
        "tipo": request.args.get("tipo"),
        "usuario_id": request.args.get("usuario_id"),
        "fecha_desde": request.args.get("fecha_desde"),
        "fecha_hasta": request.args.get("fecha_hasta"),
    }

    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))

    resultado = inventario.listar_movimientos(filtros, page, limit)

    return success_response(data=resultado)



