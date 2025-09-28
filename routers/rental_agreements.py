from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, database
from auth_dependency import get_current_user, require_role
from utils import create_audit_log

router = APIRouter(prefix="/rental_agreements", tags=["Rental Agreements"])

from sqlalchemy import func
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, database
from datetime import datetime

router = APIRouter(prefix="/rental_agreements", tags=["Rental Agreements"])

def generate_document_no(db: Session) -> str:
    year = datetime.now().year
    count = db.query(func.count(models.RentalAgreement.agreement_id)).scalar() + 1
    return f"RA-{year}-{count:03d}"


@router.post("/", response_model=schemas.AgreementResponse)
def create_agreement(payload: schemas.AgreementCreate, db: Session = Depends(database.get_db)):
    # auto-generate document_no
    doc_no = generate_document_no(db)

    new_agreement = models.RentalAgreement(
        document_no=doc_no,
        agreement_date=payload.agreement_date,
        landlord_id=payload.landlord_id,
        tenant_id=payload.tenant_id,
        place_of_signing=payload.place_of_signing,
        district=payload.district,
        province=payload.province,
        property_description=payload.property_description,
        deposit=payload.deposit,
        monthly_rent_amount=payload.monthly_rent_amount,
        monthly_due_day=payload.monthly_due_day,
        rental_start_date=payload.rental_start_date,
        rental_end_date=payload.rental_end_date,
        rental_terms=payload.rental_terms,
    )

    db.add(new_agreement)
    db.commit()
    db.refresh(new_agreement)
    return new_agreement

@router.get("/{agreement_id}", response_model=schemas.AgreementResponse)
def get_agreement(agreement_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    agreement = db.query(models.RentalAgreement).filter(models.RentalAgreement.agreement_id == agreement_id).first()
    if not agreement:
        raise HTTPException(status_code=404, detail="Agreement not found")
    if current_user.role != "admin" and agreement.landlord_id != current_user.user_id and agreement.tenant_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return agreement

@router.get("/", response_model=list[schemas.AgreementResponse])
def get_my_agreements(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role == "admin":
        # Admins see everything
        agreements = db.query(models.RentalAgreement).all()
    else:
        # Landlord/Tenant only see their agreements
        agreements = db.query(models.RentalAgreement).filter(
            (models.RentalAgreement.landlord_id == current_user.user_id) |
            (models.RentalAgreement.tenant_id == current_user.user_id)
        ).all()

    if not agreements:
        raise HTTPException(status_code=404, detail="No agreements found for this user")

    return agreements
