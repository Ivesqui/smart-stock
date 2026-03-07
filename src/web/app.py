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
# PRODUCCIÓN
# ======================================================

if __name__ == "__main__":
    # Para desarrollo únicamente
    app.run(host="0.0.0.0", port=5000)