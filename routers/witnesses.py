from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import models, schemas, database
from auth_dependency import get_current_user

router = APIRouter(prefix="/witnesses", tags=["Witnesses"])

@router.post("/", response_model=schemas.WitnessResponse)
def add_witness(payload: schemas.WitnessCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    witness = models.Witness(**payload.dict())
    db.add(witness)
    db.commit()
    db.refresh(witness)
    return witness
