from datetime import datetime
from core.entities.producto import Producto


class InventarioService:

    def __init__(self, repository):
        self.repository = repository

    # ======================================================
    # CREAR PRODUCTO
    # ======================================================
    def crear_producto(self, producto: Producto):

        if not producto.sku or not producto.nombre_producto:
            raise ValueError("SKU y nombre son obligatorios")

        if self.repository.obtener_por_sku(producto.sku):
            raise ValueError("El SKU ya existe")

        producto.fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        producto.fecha_actualizacion = producto.fecha_creacion
        producto.activo = True

        self.repository.guardar(producto)
        return True

    # ======================================================
    # LISTAR PRODUCTOS
    # ======================================================
    def listar_productos(self, estado=None):

        productos = self.repository.obtener_todos()

        if estado == "ACTIVO":
            return [p for p in productos if p["activo"] == 1]

        if estado == "INACTIVO":
            return [p for p in productos if p["activo"] == 0]

        return productos

    # ======================================================
    # BUSCAR
    # ======================================================
    def buscar_por_sku(self, sku: str):
        return self.repository.obtener_por_sku(sku)

    def buscar_por_nombre(self, nombre: str):
        return self.repository.obtener_por_nombre(nombre)

    def buscar_por_codigo_barras(self, codigo: str):
        return self.repository.obtener_por_codigo_barras(codigo)

    # ======================================================
    # ACTUALIZACIONES
    # ======================================================
    def actualizar_producto(self, sku: str, datos: dict):

        producto = self.repository.obtener_por_sku(sku)
        if not producto:
            return False

        datos["fecha_actualizacion"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.repository.actualizar(sku, datos)
        return True

    def actualizar_parcial(self, sku: str, datos: dict):

        producto = self.repository.obtener_por_sku(sku)
        if not producto:
            return False

        datos["fecha_actualizacion"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.repository.actualizar_parcial(sku, datos)
        return True

    # ======================================================
    # ACTIVAR PRODUCTO
    # ======================================================
    def activar_producto(self, sku: str):

        producto = self.repository.obtener_por_sku(sku)

        if not producto:
            return False

        self.repository.activar_logico(sku)
        return True

    # ======================================================
    # DESACTIVAR
    # ======================================================
    def desactivar_producto(self, sku: str):

        producto = self.repository.obtener_por_sku(sku)
        if not producto:
            return False

        self.repository.eliminar_logico(sku)
        return True

    # ======================================================
    # MOVIMIENTOS
    # ======================================================
    def registrar_movimiento(self, sku, tipo, cantidad, motivo):

        if cantidad <= 0:
            raise ValueError("Cantidad debe ser mayor a 0")

        producto = self.repository.obtener_por_sku(sku)
        if not producto:
            return False

        if tipo not in ["ENTRADA", "SALIDA"]:
            raise ValueError("Tipo debe ser ENTRADA o SALIDA")

        if tipo == "SALIDA" and producto["stock_actual"] < cantidad:
            raise ValueError("Stock insuficiente")

        nuevo_stock = (
            producto["stock_actual"] + cantidad
            if tipo == "ENTRADA"
            else producto["stock_actual"] - cantidad
        )

        self.repository.actualizar_parcial(sku, {
            "stock_actual": nuevo_stock,
            "fecha_actualizacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        self.repository.guardar_movimiento({
            "sku": sku,
            "tipo": tipo,
            "cantidad": cantidad,
            "motivo": motivo,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        return True

    def obtener_movimientos_por_sku(self, sku):
        return self.repository.obtener_movimientos_por_sku(sku)

    # ======================================================
    # DASHBOARD
    # ======================================================
    def obtener_resumen_dashboard(self):

        productos = self.repository.obtener_todos()

        return {
            "total_productos": len(productos),
            "productos_activos": len([p for p in productos if p["activo"] == 1]),
            "productos_bajo_stock": len([
                p for p in productos
                if p["stock_actual"] <= p["stock_minimo"]
            ])
        }