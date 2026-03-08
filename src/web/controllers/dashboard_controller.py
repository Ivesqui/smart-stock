from utils.responses import success_response
from container.dependencies import inventario

# ======================================================
# DASHBOARD
# ======================================================

def dashboard():
    resumen = inventario.obtener_resumen_dashboard()
    return success_response(data=resumen)