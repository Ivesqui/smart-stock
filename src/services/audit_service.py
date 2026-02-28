class AuditService:

    def __init__(self, audit_repo):
        self.audit_repo = audit_repo

    def log(self, user_id, action, target_user_id=None, details=None):
        self.audit_repo.crear_log(
            user_id=user_id,
            action=action,
            target_user_id=target_user_id,
            details=details
        )

    def obtener_logs(self):
        return self.audit_repo.obtener_log_todos()


