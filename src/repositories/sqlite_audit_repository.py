import sqlite3

class AuditRepository:

    def __init__(self, db_path):
        self.db_path = db_path

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def crear_log(self, user_id, action, target_user_id=None, details=None):
        conn = self._connect()
        cursor = conn.cursor()
        query = """
        INSERT INTO audit_logs (user_id, action, target_user_id, details)
        VALUES (?, ?, ?, ?)
        """
        cursor.execute(query, (user_id, action, target_user_id, details))
        conn.commit()
        conn.close()

    def obtener_log_todos(self):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, user_id, action, target_user_id, timestamp, details
                FROM audit_logs
                ORDER BY timestamp DESC
                LIMIT 100
            """)
            rows = cursor.fetchall()

        return [dict(row) for row in rows]