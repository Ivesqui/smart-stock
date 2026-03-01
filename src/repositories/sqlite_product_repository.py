import sqlite3
from typing import List, Optional


class SqliteProductRepository:

    def __init__(self, db_path):
        self.db_path = db_path

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    # ======================================================
    # GUARDAR PRODUCTO
    # ======================================================
    def save(self, producto):

        conn = self._connect()
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
    def get_all(self) -> List[dict]:
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos")
        filas = cursor.fetchall()
        conn.close()
        return [dict(fila) for fila in filas]

    # ======================================================
    # OBTENER POR SKU
    # ======================================================
    def get_by_sku(self, sku: str) -> Optional[dict]:
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos WHERE sku = ?", (sku,))
        fila = cursor.fetchone()
        conn.close()
        return dict(fila) if fila else None

    # ======================================================
    # BUSCAR POR NOMBRE
    # ======================================================
    def get_by_name(self, nombre: str):
        conn = self._connect()
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
    def get_by_barcode(self, codigo: str):
        conn = self._connect()
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
    def update_all(self, sku: str, datos: dict):
        conn = self._connect()
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
        self.update_all(sku, datos)

    # ======================================================
    # ELIMINACIÓN LÓGICA
    # ======================================================
    def delete_logic(self, sku: str):
        conn = self._connect()
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
    def activate_logic(self, sku: str):
        conn = self._connect()
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
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO movimientos (
                sku, tipo, cantidad, motivo, usuario_id, fecha
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            movimiento["sku"],
            movimiento["tipo"],
            movimiento["cantidad"],
            movimiento["motivo"],
            movimiento["usuario_id"],
            movimiento["fecha"]
        ))
        conn.commit()
        conn.close()

    # Obtener movimientos por sku

    def obtener_movimientos_por_sku(self, sku: str):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM movimientos
            WHERE sku = ?
            ORDER BY fecha DESC
        """, (sku,))
        filas = cursor.fetchall()
        conn.close()
        return [dict(fila) for fila in filas]

    # Obtener movimientos

    def obtener_movimientos(self, filtros, page, limit):

        conn = self._connect()
        cursor = conn.cursor()
        query = """
            SELECT id, sku, tipo, cantidad, motivo, usuario_id, fecha
            FROM movimientos
            WHERE 1=1
        """

        cursor.execute(query)

        params = []

        if filtros.get("sku"):
            query += " AND sku = ?"
            params.append(filtros["sku"])

        if filtros.get("tipo"):
            query += " AND tipo = ?"
            params.append(filtros["tipo"])

        if filtros.get("usuario_id"):
            query += " AND usuario_id = ?"
            params.append(filtros["usuario_id"])

        if filtros.get("fecha_desde"):
            query += " AND fecha >= ?"
            params.append(filtros["fecha_desde"])

        if filtros.get("fecha_hasta"):
            query += " AND fecha <= ?"
            params.append(filtros["fecha_hasta"])

        # PAGINACIÓN
        offset = (page - 1) * limit
        query += " ORDER BY fecha DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])


        cursor.execute(query, params)
        rows = cursor.fetchall()

        movimientos = []

        for row in rows:
            movimientos.append({
                "id": row[0],
                "sku": row[1],
                "tipo": row[2],
                "cantidad": row[3],
                "motivo": row[4],
                "usuario_id": row[5],
                "fecha": row[6]
            })

        return movimientos

    # Obtener stock crítico
    def obtener_stock_critico(self):

        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT sku, nombre_producto, stock_actual, stock_minimo
                FROM productos
                WHERE stock_actual <= stock_minimo
                ORDER BY stock_actual ASC
            """)
            rows = cursor.fetchall()

        productos = []

        for row in rows:
            stock_actual = row["stock_actual"]
            stock_minimo = row["stock_minimo"]

            # porcentaje respecto al mínimo
            porcentaje_restante = (
                round((stock_actual / stock_minimo) * 100, 2)
                if stock_minimo > 0 else 0
            )

            # 🚨 niveles más inteligentes
            if stock_actual == 0:
                nivel = "AGOTADO"
            elif porcentaje_restante <= 50:
                nivel = "CRITICO"
            else:
                nivel = "BAJO"

            productos.append({
                "sku": row["sku"],
                "nombre": row["nombre_producto"],
                "stock_actual": stock_actual,
                "stock_minimo": stock_minimo,
                "porcentaje_minimo": porcentaje_restante,
                "nivel_alerta": nivel
            })

        return {
        "total_alertas": len(productos),
        "data": productos
        }