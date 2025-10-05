from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, List

class UserRegister(BaseModel):
    firstname: str
    lastname: str
    email: str
    password: str
    role: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    user_id: int
    firstname: str
    lastname: str
    role: str
    email: str
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    role: str
class AgreementBase(BaseModel):
    agreement_date: date
    landlord_id: int
    tenant_id: int
    place_of_signing: Optional[str]
    district: Optional[str]
    province: Optional[str]
    property_description: Optional[str]
    deposit: Optional[float]
    monthly_rent_amount: float
    monthly_due_day: Optional[int]
    rental_start_date: date
    rental_end_date: date
    rental_terms: Optional[str]

class AgreementCreate(AgreementBase):
    pass

class AuditLogResponse(BaseModel):
    log_id: int
    action: str
    details: Optional[str]
    created_at: datetime
    user_id: int
    class Config:
        orm_mode = True

class AgreementResponse(BaseModel):
    agreement_id: int
    document_no: str
    agreement_date: date
    landlord_id: int
    tenant_id: int
    place_of_signing: Optional[str] = None
    district: Optional[str] = None
    province: Optional[str] = None
    property_description: Optional[str] = None
    deposit: Optional[float] = None
    monthly_rent_amount: float
    monthly_due_day: Optional[int] = None
    rental_start_date: date
    rental_end_date: date
    rental_terms: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime
    audit_logs: list[AuditLogResponse] = []   # ✅ typed properly

    class Config:
        orm_mode = True

class WitnessCreate(BaseModel):
    agreement_id: int
    name: str
    address: Optional[str]

class WitnessResponse(WitnessCreate):
    witness_id: int
    class Config:
        orm_mode = True
