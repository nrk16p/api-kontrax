from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, DECIMAL, TIMESTAMP
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    role = Column(String(50))
    firstname = Column(String(100))
    lastname = Column(String(100))
    age = Column(Integer, nullable=True)
    idcard_no = Column(String(20), unique=True, nullable=True)
    address = Column(Text, nullable=True)
    phone_number = Column(String(30), nullable=True)
    email = Column(String(150), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())
    agreements_as_landlord = relationship("RentalAgreement", foreign_keys="[RentalAgreement.landlord_id]")
    agreements_as_tenant = relationship("RentalAgreement", foreign_keys="[RentalAgreement.tenant_id]")

class RentalAgreement(Base):
    __tablename__ = "rental_agreements"

    agreement_id = Column(Integer, primary_key=True, index=True)
    document_no = Column(String(50), unique=True, nullable=False)
    agreement_date = Column(Date, nullable=False)

    landlord_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    tenant_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    place_of_signing = Column(String(255), nullable=False)
    district = Column(String(100), nullable=False)
    province = Column(String(100), nullable=False)
    property_description = Column(Text, nullable=False)

    deposit = Column(DECIMAL(15, 2), nullable=False)
    monthly_rent_amount = Column(DECIMAL(15, 2), nullable=False)
    monthly_due_day = Column(Integer, nullable=False)
    rental_start_date = Column(Date, nullable=False)
    rental_end_date = Column(Date, nullable=False)

    rental_terms = Column(Text, nullable=True)
    status = Column(String(50), server_default="draft")   # ✅ server default

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())   # ✅ auto insert
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())  # ✅ auto update

    # relationships
    witnesses = relationship("Witness", back_populates="agreement")
    signatures = relationship("Signature", back_populates="agreement")
  
    audit_logs = relationship("AuditLog", back_populates="agreement", cascade="all, delete-orphan")
class Witness(Base):
    __tablename__ = "witnesses"
    witness_id = Column(Integer, primary_key=True, index=True)
    agreement_id = Column(Integer, ForeignKey("rental_agreements.agreement_id"))
    name = Column(String(150))
    address = Column(Text)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    agreement = relationship("RentalAgreement", back_populates="witnesses")

class Signature(Base):
    __tablename__ = "signatures"
    signature_id = Column(Integer, primary_key=True, index=True)
    agreement_id = Column(Integer, ForeignKey("rental_agreements.agreement_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    witness_id = Column(Integer, ForeignKey("witnesses.witness_id"), nullable=True)
    role = Column(String(50))
    signature_file = Column(String(255))
    signed_at = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
    agreement = relationship("RentalAgreement", back_populates="signatures")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    log_id = Column(Integer, primary_key=True, index=True)
    agreement_id = Column(Integer, ForeignKey("rental_agreements.agreement_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    action = Column(String(100))
    details = Column(Text)
    created_at = Column(TIMESTAMP)
    agreement = relationship("RentalAgreement", back_populates="audit_logs")
    user = relationship("User")
