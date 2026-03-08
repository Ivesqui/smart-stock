import os

from repositories.sqlite_product_repository import SqliteProductRepository
from repositories.sqlite_user_repository import SqliteUserRepository
from repositories.sqlite_audit_repository import AuditRepository
from services.inventory_service import InventoryService
from services.auth_service import AuthService
from services.user_service import UserService
from services.audit_service import AuditService
from services.reports_excel_service import InventoryExcelService


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "inventario.db")


repo = SqliteProductRepository(DB_PATH)
inventario = InventoryService(repo)

usuario_repo = SqliteUserRepository(DB_PATH)
auth_service = AuthService(usuario_repo)

user_service = UserService(usuario_repo)

audit_repo = AuditRepository(DB_PATH)
audit_serv = AuditService(audit_repo)

excel_service = InventoryExcelService(inventario)