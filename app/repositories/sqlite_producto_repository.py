import sqlite3
from typing import List, Optional


class SqliteProductoRepository:

    def __init__(self, db_path="inventario.db"):
        self.db_path = db_path

    def _conectar(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    # ======================================================
    # GUARDAR PRODUCTO
    # ======================================================
    def guardar(self, producto):

        conn = self._conectar()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO productos (
                sku, codigo_barras, nombre_producto, categoria,
                descripcion, unidad, precio_compra, precio_venta,
                stock_actual, stock_minimo, activo,
                fecha_creacion, fecha_actualizacion
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            producto.sku,
            producto.codigo_barras,
            producto.nombre_producto,
            producto.categoria,
            producto.descripcion,
            producto.unidad,
            producto.precio_compra,
            producto.precio_venta,
            producto.stock_actual,
            producto.stock_minimo,
            int(producto.activo),
            producto.fecha_creacion,
            producto.fecha_actualizacion
        ))

        conn.commit()
        conn.close()

    # ======================================================
    # OBTENER TODOS
    # ======================================================
    def obtener_todos(self) -> List[dict]:
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos")
        filas = cursor.fetchall()
        conn.close()
        return [dict(fila) for fila in filas]

    # ======================================================
    # OBTENER POR SKU
    # ======================================================
    def obtener_por_sku(self, sku: str) -> Optional[dict]:
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos WHERE sku = ?", (sku,))
        fila = cursor.fetchone()
        conn.close()
        return dict(fila) if fila else None

    # ======================================================
    # BUSCAR POR NOMBRE
    # ======================================================
    def obtener_por_nombre(self, nombre: str):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM productos
            WHERE nombre_producto LIKE ?
        """, (f"%{nombre}%",))
        filas = cursor.fetchall()
        conn.close()
        return [dict(fila) for fila in filas]

    # ======================================================
    # BUSCAR POR CÓDIGO DE BARRAS
    # ======================================================
    def obtener_por_codigo_barras(self, codigo: str):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM productos
            WHERE codigo_barras = ?
        """, (codigo,))
        fila = cursor.fetchone()
        conn.close()
        return dict(fila) if fila else None

    # ======================================================
    # ACTUALIZAR
    # ======================================================
    def actualizar(self, sku: str, datos: dict):
        conn = self._conectar()
        cursor = conn.cursor()

        campos = ", ".join([f"{k} = ?" for k in datos.keys()])
        valores = list(datos.values())

        cursor.execute(
            f"UPDATE productos SET {campos} WHERE sku = ?",
            valores + [sku]
        )

        conn.commit()
        conn.close()

    def actualizar_parcial(self, sku: str, datos: dict):
        self.actualizar(sku, datos)

    # ======================================================
    # ELIMINACIÓN LÓGICA
    # ======================================================
    def eliminar_logico(self, sku: str):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE productos
            SET activo = 0
            WHERE sku = ?
        """, (sku,))
        conn.commit()
        conn.close()

    # ======================================================
    # ACTIVAR PRODUCTO (ALTA LÓGICA)
    # ======================================================
    def activar_logico(self, sku: str):
        conn = self._conectar()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE productos
            SET activo = 1
            WHERE sku = ?
        """, (sku,))

        conn.commit()
        conn.close()

    # ======================================================
    # MOVIMIENTOS
    # ======================================================
    def guardar_movimiento(self, movimiento: dict):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO movimientos (
                sku, tipo, cantidad, motivo, fecha
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            movimiento["sku"],
            movimiento["tipo"],
            movimiento["cantidad"],
            movimiento["motivo"],
            movimiento["fecha"]
        ))
        conn.commit()
        conn.close()

    def obtener_movimientos_por_sku(self, sku: str):
        conn = self._conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM movimientos
            WHERE sku = ?
            ORDER BY fecha DESC
        """, (sku,))
        filas = cursor.fetchall()
        conn.close()
        return [dict(fila) for fila in filas]