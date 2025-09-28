from sqlalchemy.orm import Session
import models
from datetime import datetime

def create_audit_log(db: Session, agreement_id: int, user_id: int, action: str, details: str = None):
    log = models.AuditLog(
        agreement_id=agreement_id,
        user_id=user_id,
        action=action,
        details=details,
        created_at=datetime.utcnow()
    )
    db.add(log)
    db.commit()
    return log
