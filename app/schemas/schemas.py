from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Kullanıcı Kayıt Şeması
class UserCreate(BaseModel):
    tc_no: str
    full_name: str
    password: str
    role: str = "patient" # Varsayılan olarak hasta

# Kullanıcı Login Şeması
class UserLogin(BaseModel):
    tc_no: str
    password: str

# Randevu Şeması (Doktorun göreceği liste için)
class AppointmentView(BaseModel):
    id: int
    patient_name: str
    appointment_date: datetime
    status: str

    class Config:
        from_attributes = True