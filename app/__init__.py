from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='../templates')
    app.secret_key = 'cok_gizli_mhrs_anahtari'
    
    # MariaDB Veritabanı Bağlantısı (3307 portunu dinlediğimizi unutma)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345@db:3306/mhrs'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)

    # --- MODELLER ---
    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), nullable=False)
        email = db.Column(db.String(100), unique=True, nullable=False)
        password = db.Column(db.String(200), nullable=False)

    class Doctor(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), nullable=False)
        department = db.Column(db.String(100), nullable=False)

    class Appointment(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
        doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
        date = db.Column(db.String(50), nullable=False)
        
        doctor = db.relationship('Doctor', backref=db.backref('appointments', lazy=True))

    # --- ROUTE'LAR (SAYFALAR) ---
    @app.route('/', methods=['GET', 'POST'])
    def index():
        if 'user_id' in session:
            return redirect(url_for('dashboard'))

        if request.method == 'POST':
            action = request.form.get('action')
            email = request.form.get('email')
            password = request.form.get('password')

            if action == 'register':
                name = request.form.get('name')
                existing_user = User.query.filter_by(email=email).first()
                if existing_user:
                    flash('Bu e-posta zaten kayıtlı!', 'danger')
                else:
                    hashed_pw = generate_password_hash(password)
                    new_user = User(name=name, email=email, password=hashed_pw)
                    db.session.add(new_user)
                    db.session.commit()
                    flash('Kayıt başarılı! Şimdi giriş yapabilirsiniz.', 'success')
            
            elif action == 'login':
                user = User.query.filter_by(email=email).first()
                if user and check_password_hash(user.password, password):
                    session['user_id'] = user.id
                    session['user_name'] = user.name
                    return redirect(url_for('dashboard'))
                else:
                    flash('Hatalı e-posta veya şifre!', 'danger')

        return render_template('index.html')

    @app.route('/dashboard', methods=['GET', 'POST'])
    def dashboard():
        if 'user_id' not in session:
            return redirect(url_for('index'))

        if request.method == 'POST':
            doctor_id = request.form.get('doctor_id')
            date = request.form.get('date')
            new_apt = Appointment(user_id=session['user_id'], doctor_id=doctor_id, date=date)
            db.session.add(new_apt)
            db.session.commit()
            flash('Randevunuz başarıyla oluşturuldu!', 'success')
            return redirect(url_for('dashboard'))

        doctors = Doctor.query.all()
        appointments = Appointment.query.filter_by(user_id=session['user_id']).all()
        return render_template('dashboard.html', doctors=doctors, appointments=appointments, user_name=session['user_name'])

    @app.route('/logout')
    def logout():
        session.pop('user_id', None)
        session.pop('user_name', None)
        return redirect(url_for('index'))

    return app