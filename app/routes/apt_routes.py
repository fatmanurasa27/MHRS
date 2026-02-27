from flask import Blueprint, request, jsonify
from ..models.models import Appointment
from ..db.session import db
from datetime import datetime

apt_bp = Blueprint('apt_bp', __name__)

@apt_bp.route('/my-appointments/<int:user_id>', methods=['GET'])
def get_my_appointments(user_id):
    try:
        # Randevuları en yeni en üstte olacak şekilde çekiyoruz
        apts = Appointment.query.filter_by(patient_id=user_id).order_by(Appointment.appointment_date.desc()).all()
        return jsonify([{
            "id": a.id,
            "department": a.department,
            "doctor_name": a.doctor_name,
            "date": a.appointment_date.strftime("%d.%m.%Y %H:%M"),
            "raw_date": a.appointment_date.isoformat()
        } for a in apts])
    except Exception as e:
        return jsonify({"error": "Liste çekilemedi"}), 500

@apt_bp.route('/book', methods=['POST'])
def book():
    data = request.get_json()
    try:
        # Tarihi Python formatına çeviriyoruz
        date_obj = datetime.strptime(data['date'], "%Y-%m-%dT%H:%M")
        new_apt = Appointment(
            patient_id=data['patient_id'],
            department=data['department'],
            doctor_name=data['doctor'], # HTML'den gelen doktor ismi
            appointment_date=date_obj
        )
        db.session.add(new_apt)
        db.session.commit()
        return jsonify({"msg": "Başarılı"}), 201
    except Exception as e:
        return jsonify({"error": "Kayıt hatası"}), 400