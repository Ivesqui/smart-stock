from utils.responses import success_response
from container.dependencies import inventario

# ALERTAS

def alerta_stock_critico():
    productos = inventario.obtener_stock_critico()
    return success_response(data=productos)