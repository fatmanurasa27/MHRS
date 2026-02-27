from fastapi import FastAPI
from app.db.session import engine
from app.models import models
from app.api.endpoints import auth # Yeni ekledik

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="MHRS Hastane Sistemi")

# Route'ları dahil et
app.include_router(auth.router, prefix="/auth", tags=["Giriş İşlemleri"])

@app.get("/")
def home():
    return {"message": "MHRS API Aktif!"}