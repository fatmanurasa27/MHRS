from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...db.session import get_db
from ...models import models
from ...schemas import schemas

router = APIRouter()

@router.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # TC No zaten kayıtlı mı kontrol et
    db_user = db.query(models.User).filter(models.User.tc_no == user.tc_no).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Bu TC ile zaten kayıt olunmuş.")
    
    new_user = models.User(
        tc_no=user.tc_no,
        full_name=user.full_name,
        password=user.password,
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Kayıt başarılı", "user": new_user.full_name}

@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(
        models.User.tc_no == user.tc_no, 
        models.User.password == user.password
    ).first()
    
    if not db_user:
        raise HTTPException(status_code=401, detail="Hatalı TC veya şifre")
    
    return {
        "message": f"Hoş geldiniz {db_user.full_name}",
        "role": db_user.role,
        "id": db_user.id
    }