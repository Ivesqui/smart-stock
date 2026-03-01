import sqlite3


def connect():
    """
    Crea y devuelve una conexión a la base de datos SQLite.

    Mejoras aplicadas:
    - row_factory permite acceder a columnas por nombre
    - Se activan foreign keys (SQLite las tiene desactivadas por defecto)
    """

    conn = sqlite3.connect("inventario.db")

    # Permite acceder como diccionario: row["campo"]
    conn.row_factory = sqlite3.Row

    # Activar claves foráneas
    conn.execute("PRAGMA foreign_keys = ON;")

    return conn


def create_tables():
    """
    Crea las tablas principales del sistema.

    Diseño:
    - productos → estado actual del inventario
    - movimientos → historial completo (kardex)
    """

    conn = connect()
    cursor = conn.cursor()

    # ==========================================================
    # TABLA: productos
    # ==========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sku TEXT UNIQUE NOT NULL,
            codigo_barras TEXT UNIQUE,
            nombre_producto TEXT NOT NULL,
            categoria TEXT NOT NULL,
            descripcion TEXT,
            unidad TEXT NOT NULL,
            precio_compra REAL NOT NULL,
            precio_venta REAL NOT NULL,
            stock_actual INTEGER NOT NULL,
            stock_minimo INTEGER NOT NULL,
            activo INTEGER NOT NULL DEFAULT 1,
            fecha_creacion TEXT NOT NULL,
            fecha_actualizacion TEXT NOT NULL
        )
    """)

    # ==========================================================
    # TABLA: movimientos
    # ==========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movimientos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sku TEXT NOT NULL,
            tipo TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            motivo TEXT NOT NULL,
            usuario_id INTEGER NOT NULL,
            fecha TEXT NOT NULL,
            FOREIGN KEY (sku) REFERENCES productos(sku)
                ON DELETE CASCADE
        )
    """)

    # ==========================================================
    # TABLA: Usuarios
    # ==========================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            rol TEXT NOT NULL, -- ADMIN | OPERADOR
            activo INTEGER NOT NULL DEFAULT 1,
            fecha_creacion TEXT NOT NULL
        )
    """)

    # ==========================================================
    # TABLA: audit_logs
    # ==========================================================
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,           
        action TEXT NOT NULL,             
        target_user_id INTEGER,            
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        details TEXT
    );
    """)

    # CREAR ÍNDICE EN AUDIT LOGS

    cursor.execute("""
    CREATE INDEX idx_audit_timestamp ON audit_logs(timestamp);
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sync_queue (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        entity TEXT,              
        entity_id INTEGER,        
        action TEXT,              
        payload TEXT,             
        synced INTEGER DEFAULT 0, 
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );""")

    conn.commit()
    conn.close()
