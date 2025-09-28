from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import models, database
from auth_dependency import get_current_user
from utils import create_audit_log

router = APIRouter(prefix="/signatures", tags=["Signatures"])

@router.post("/{agreement_id}")
def sign_agreement(agreement_id: int, file: UploadFile = File(...), db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    agreement = db.query(models.RentalAgreement).filter(models.RentalAgreement.agreement_id == agreement_id).first()
    if not agreement:
        raise HTTPException(status_code=404, detail="Agreement not found")
    if current_user.role == "landlord" and agreement.lender_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to sign as landlord")
    if current_user.role == "tenant" and agreement.borrower_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to sign as tenant")
    file_path = f"signatures/{current_user.user_id}_{file.filename}"
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    signature = models.Signature(agreement_id=agreement_id, user_id=current_user.user_id, role=current_user.role, signature_file=file_path)
    db.add(signature)
    db.commit()
    db.refresh(signature)
    create_audit_log(db, agreement_id, current_user.user_id, "signed", f"{current_user.role} signed")
    return {"message": "Signature saved", "signature_id": signature.signature_id}
