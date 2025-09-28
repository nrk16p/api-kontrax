from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, database
from auth_dependency import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=list[schemas.UserResponse])
def list_users(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.User).all()
