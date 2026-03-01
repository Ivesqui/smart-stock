# ======================================================
# API WEB - SISTEMA DE INVENTARIO
# ======================================================
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import send_file
from flask import g
from core.entities.product import Product
from services.auth_service import AuthService
from services.inventory_service import InventoryService
from services.reports_excel_service import InventoryExcelService
from repositories.sqlite_product_repository import SqliteProductRepository
from repositories.sqlite_user_repository import SqliteUserRepository
from security.decorators import token_required, roles_required
from services.user_service import UserService
from services.audit_service import AuditService
from repositories.sqlite_audit_repository import AuditRepository


# ======================================================
# CONFIGURACIÓN
# ======================================================

app = Flask(__name__)
CORS(app)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "inventario.db")
repo = SqliteProductRepository(DB_PATH)
inventario = InventoryService(repo)
usuario_repo = SqliteUserRepository(DB_PATH)
auth_service = AuthService(usuario_repo)
excel_service = InventoryExcelService(inventario)
user_service = UserService(usuario_repo)
audit_repo = AuditRepository(DB_PATH)
audit_serv = AuditService(audit_repo)

# ======================================================
# RESPUESTAS ESTÁNDAR
# ======================================================

def success_response(data=None, message=None, status=200):
    response = {}
    if message:
        response["message"] = message
    if data is not None:
        response["data"] = data
    return jsonify(response), status


def error_response(message, status=400):
    return jsonify({"error": message}), status

# ======================================================
# AUTH
# ======================================================

@app.route("/auth/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        if not data:
            return error_response("Datos requeridos", 400)

        usuario = auth_service.registrar(
            nombre=data["nombre"],
            email=data["email"],
            password=data["password"],
            rol=data.get("rol", "OPERADOR")
        )

        return success_response(
            data=usuario.to_dict(),
            message="User registrado",
            status=201
        )

    except ValueError as e:
        return error_response(str(e), 400)
    #except Exception:
    #    return error_response("Error interno del servidor", 500)
    except Exception as e:
        print("ERROR REGISTER:", e)
        raise



@app.route("/auth/login", methods=["POST"])
def login():
    try:
        data = request.get_json()

        token = auth_service.login(
            email=data["email"],
            password=data["password"]
        )

        return success_response(data={"token": token})

    except ValueError as e:
        return error_response(str(e), 401)

    except Exception as e:
        print("ERROR LOGIN:", e)
        raise


# ======================================================
# PRODUCTOS
# ======================================================

# ✔ Crear product
@app.route("/productos", methods=["POST"])
@token_required
@roles_required("ADMIN", "OPERADOR")
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
@app.route("/productos", methods=["GET"])
@token_required
@roles_required("ADMIN", "OPERADOR")
def listar_productos():

    estado = request.args.get("estado")  # ACTIVO / INACTIVO

    productos = inventario.listar_productos(estado)

    return success_response(data=productos)


# ✔ Buscar por SKU
@app.route("/productos/<sku>", methods=["GET"])
@token_required
@roles_required("ADMIN", "OPERADOR")
def buscar_por_sku(sku):

    producto = inventario.buscar_por_sku(sku)

    if not producto:
        return error_response("Product no encontrado", 404)

    return success_response(data=producto)


# ✔ Buscar por nombre
@app.route("/productos/nombre/<nombre>", methods=["GET"])
@token_required
@roles_required("ADMIN", "OPERADOR")
def buscar_por_nombre(nombre):

    productos = inventario.buscar_por_nombre(nombre)

    return success_response(data=productos)


# ✔ Buscar por código de barras
@app.route("/productos/barcode/<codigo>", methods=["GET"])
@token_required
@roles_required("ADMIN", "OPERADOR")
def buscar_por_codigo(codigo):

    producto = inventario.buscar_por_codigo_barras(codigo)

    if not producto:
        return error_response("Product no encontrado", 404)

    return success_response(data=producto)


# ✔ PUT total
@app.route("/productos/<sku>", methods=["PUT"])
@token_required
@roles_required("ADMIN", "OPERADOR")
def actualizar_total(sku):

    data = request.get_json()

    actualizado = inventario.actualizar_producto(sku, data)

    if not actualizado:
        return error_response("Product no encontrado", 404)

    return success_response(message="Product actualizado")


# ✔ PATCH parcial
@app.route("/productos/<sku>", methods=["PATCH"])
@token_required
@roles_required("ADMIN", "OPERADOR")
def actualizar_parcial(sku):

    data = request.get_json()

    actualizado = inventario.actualizar_parcial(sku, data)

    if not actualizado:
        return error_response("Product no encontrado", 404)

    return success_response(message="Product actualizado parcialmente")

# ✔ PATCH alta lógica
@app.route("/productos/<sku>/alta", methods=["PATCH"])
@token_required
@roles_required("ADMIN", "OPERADOR")
def dar_de_alta(sku):

    activado = inventario.activar_producto(sku)

    if not activado:
        return error_response("Product no encontrado", 404)

    return success_response(message="Product activado")

# ✔ PATCH baja lógica
@app.route("/productos/<sku>/baja", methods=["PATCH"])
@token_required
@roles_required("ADMIN", "OPERADOR")
def dar_de_baja(sku):

    eliminado = inventario.desactivar_producto(sku)

    if not eliminado:
        return error_response("Product no encontrado", 404)

    return success_response(message="Product desactivado")


# ======================================================
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
# DASHBOARD
# ======================================================

@app.route("/dashboard/resumen", methods=["GET"])
@token_required # <- autenticación
@roles_required("ADMIN")
def dashboard():

    resumen = inventario.obtener_resumen_dashboard()

    return success_response(data=resumen)

# ======================================================
# REPORTE INVENTARIO EXCEL
# ======================================================

@app.route("/reportes/inventario/excel", methods=["GET"])
@token_required # <- autenticación
@roles_required("ADMIN", "OPERADOR")
def descargar_excel_inventario():

    archivo_excel = excel_service.generar_excel_en_memoria()

    return send_file(
        archivo_excel,
        as_attachment=True,
        download_name="reporte_inventario.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# ======================================================
# GESTIÓN DE USUARIOS
# ======================================================

#ADMIN

# Listar todos los usuarios
@app.route("/users", methods=["GET"])
@token_required
@roles_required("ADMIN")
def listar_usuarios():

    usuarios = user_service.listar_usuarios()
    return success_response(data=[u.to_dict() for u in usuarios])

# Obtener usuario por id
@app.route("/users/<int:user_id>", methods=["GET"])
@token_required
@roles_required("ADMIN")
def obtener_usuario(user_id):

    usuario = user_service.obtener_por_id(user_id)
    return success_response(data=usuario.to_dict())

# Cambiar rol de usuario
@app.route("/users/<int:user_id>/role", methods=["PATCH"])
@token_required
@roles_required("ADMIN")
def cambiar_rol(user_id):

    data = request.get_json()
    current_user = g.user

    user_service.cambiar_rol(
        user_id,
        data["rol"],
        current_user
    )

    return success_response(message="Rol actualizado")

# Desactivar usuario
@app.route("/users/<int:user_id>/deactivate", methods=["PATCH"])
@token_required
@roles_required("ADMIN")
def desactivar_usuario(user_id):

    current_user = g.user
    user_service.desactivar_usuario(user_id, current_user)

    return success_response(message="Usuario desactivado")

# Activar usuario
@app.route("/users/<int:user_id>/activate", methods=["PATCH"])
@token_required
@roles_required("ADMIN")
def activar_usuario(user_id):

    user_service.activar_usuario(user_id)

    return success_response(message="Usuario activado")

# Obtener logs de auditoria

@app.route("/admin/audit-logs", methods=["GET"])
@token_required
@roles_required("ADMIN")
def obtener_audit_logs():

    logs = audit_serv.obtener_logs()
    return success_response(data=logs)


# Información de usuario
@app.route("/auth/me", methods=["GET"])
@token_required
def obtener_usuario_actual():

    current_user = g.user
    usuario = user_service.obtener_por_id(current_user["user_id"])

    return success_response(data=usuario.to_dict())

# ======================================================
# ALERTAS
# ======================================================
@app.route("/alertas/stock-critico", methods=["GET"])
@token_required
@roles_required("ADMIN", "OPERADOR")
def alertas_stock_critico():
    productos = inventario.obtener_stock_critico()
    return success_response(data=productos)


# ======================================================
# PAGINACIÓN
# ======================================================
@app.route("/movimientos", methods=["GET"])
@token_required
@roles_required("ADMIN", "OPERADOR")
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


# ======================================================
# PRODUCCIÓN
# ======================================================

if __name__ == "__main__":
    # Para desarrollo únicamente
    app.run(host="0.0.0.0", port=5000)