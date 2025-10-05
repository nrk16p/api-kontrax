from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, schemas, database
from auth import hash_password, verify_password, create_access_token



router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=schemas.UserResponse)
def register(payload: schemas.UserRegister, db: Session = Depends(database.get_db)):
    if db.query(models.User).filter(models.User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = models.User(
        firstname=payload.firstname,
        lastname=payload.lastname,
        email=payload.email,
        role=payload.role,
        password_hash=hash_password(payload.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=schemas.Token)
def login(payload: schemas.UserLogin, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == payload.email).first()

    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # ✅ create token that contains user_id and role in payload
    token_data = {"sub": str(user.user_id), "role": user.role}
    token = create_access_token(token_data)

    # ✅ return both token and user info
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.user_id,
        "role": user.role
    }
