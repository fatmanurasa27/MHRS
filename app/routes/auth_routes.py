from flask import Blueprint, request, jsonify
from ..models.models import User
from ..db.session import db

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    new_user = User(tc_no=data['tc_no'], full_name=data['full_name'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "Kayıt Başarılı"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(tc_no=data['tc_no'], password=data['password']).first()
    if not user: return jsonify({"msg": "Hata"}), 401
    return jsonify({"id": user.id, "name": user.full_name})