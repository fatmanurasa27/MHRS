from ..db.session import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    tc_no = db.Column(db.String(11), unique=True, nullable=False)
    full_name = db.Column(db.String(100))
    password = db.Column(db.String(255))
    role = db.Column(db.String(20), default="patient")

class Appointment(db.Model):
    __tablename__ = "appointments"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    department = db.Column(db.String(100))
    doctor_name = db.Column(db.String(100)) # 400 hatasını bu alanın eksikliği yapıyordu
    appointment_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default="Aktif")