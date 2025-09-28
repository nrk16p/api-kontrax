from fastapi import FastAPI
from database import Base, engine
from routers import auth, users, rental_agreements, witnesses, signatures, audit
import models   # 👈 add this to register tables
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Rental Agreement API")

# ✅ CORS middleware (important for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],  # allow all HTTP methods
    allow_headers=["*"],  # allow Authorization, Content-Type, etc.
)

# Routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(rental_agreements.router)
app.include_router(witnesses.router)
app.include_router(signatures.router)
app.include_router(audit.router)


@app.get("/")
def root():
    return {"message": "Agreement API is running 🚀"}
