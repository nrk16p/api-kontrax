from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import models, database
from auth_dependency import get_current_user

router = APIRouter(prefix="/audit", tags=["Audit Logs"])

@router.get("/{agreement_id}")
def get_audit_logs(agreement_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.AuditLog).filter(models.AuditLog.agreement_id == agreement_id).all()
