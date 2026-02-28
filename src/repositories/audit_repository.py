class AuditRepository:

    def __init__(self, db):
        self.db = db

    def crear_log(self, user_id, action, target_user_id=None, details=None):
        query = """
        INSERT INTO audit_logs (user_id, action, target_user_id, details)
        VALUES (?, ?, ?, ?)
        """
        cursor = self.db.cursor()
        cursor.execute(query, (user_id, action, target_user_id, details))
        self.db.commit()

    def obtener_log_todos(self):
        query = """
        SELECT id, user_id, action, target_user_id, timestamp, details
        FROM audit_logs
        ORDER BY timestamp DESC
        LIMIT 100
        """
        cursor = self.db.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        logs = []
        for row in rows:
            logs.append({
                "id": row[0],
                "user_id": row[1],
                "action": row[2],
                "target_user_id": row[3],
                "timestamp": row[4],
                "details": row[5]
            })

        return logs