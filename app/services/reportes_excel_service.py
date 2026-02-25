import pandas as pd
import io
from datetime import datetime


class InventarioExcelService:

    def __init__(self, inventario_service):
        self.service = inventario_service

    def generar_excel_en_memoria(self):
        productos = self.service.listar_productos()

        data = []
        for p in productos:
            estado_stock = "CRÍTICO" if p["stock_actual"] <= p["stock_minimo"] else "OK"
            margen_unitario = p["precio_venta"] - p["precio_compra"]
            margen_total = margen_unitario * p["stock_actual"]

            data.append({
                "SKU": p["sku"],
                "Nombre": p["nombre_producto"],
                "Categoría": p["categoria"],
                "Unidad": p["unidad"],
                "Precio Compra": p["precio_compra"],
                "Precio Venta": p["precio_venta"],
                "Stock Actual": p["stock_actual"],
                "Stock Mínimo": p["stock_minimo"],
                "Valor Inventario": p["stock_actual"] * p["precio_compra"],
                "Estado Stock": estado_stock,
                "Margen Unitario": margen_unitario,
                "Margen Total": margen_total,
                "Fecha Reporte": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

        df = pd.DataFrame(data)

        output = io.BytesIO()

        # ✔ Forma correcta para evitar warning
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Inventario")

        output.seek(0)

        return output