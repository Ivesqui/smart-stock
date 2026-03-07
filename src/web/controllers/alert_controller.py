from security.decorators import token_required
from utils.responses import success_response

# ======================================================
# ALERTAS
# ======================================================
@app.route("/alertas/stock-critico", methods=["GET"])
@token_required
@roles_required("ADMIN", "OPERADOR")
def alertas_stock_critico():
    productos = inventario.obtener_stock_critico()
    return success_response(data=productos)