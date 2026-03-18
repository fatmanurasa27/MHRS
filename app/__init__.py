from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='../templates')
    app.secret_key = 'cok_gizli_mhrs_anahtari'
    
    # MariaDB Veritabanı Bağlantısı
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
        email = db.Column(db.String(100), unique=True, nullable=False)
        password = db.Column(db.String(200), nullable=False)

    class Appointment(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
        doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
        date = db.Column(db.String(50), nullable=False)
        
        doctor = db.relationship('Doctor', backref=db.backref('appointments', lazy=True))
        patient = db.relationship('User', backref=db.backref('appointments', lazy=True))

    # --- TABLOLARI VE DOKTORLARI OTOMATİK OLUŞTUR ---
    with app.app_context():
        db.create_all() 
        
        if not Doctor.query.first():
            # Doktorlara giriş yapabilmeleri için otomatik e-posta ve şifre atıyoruz
            doc_data = [
                ('Dr. Ali Yılmaz', 'Kardiyoloji', 'ali@mhrs.com'),
                ('Dr. Ayşe Demir', 'Kardiyoloji', 'ayse@mhrs.com'),
                ('Dr. Mehmet Kaya', 'Nöroloji', 'mehmet@mhrs.com'),
                ('Dr. Fatma Çelik', 'Nöroloji', 'fatma@mhrs.com')
            ]
            hashed_pw = generate_password_hash('12345') # Tüm doktorların şifresi 12345
            docs = [Doctor(name=d[0], department=d[1], email=d[2], password=hashed_pw) for d in doc_data]
            db.session.bulk_save_objects(docs)
            db.session.commit()

    # --- HASTA SAYFALARI ---
    @app.route('/', methods=['GET', 'POST'])
    def index():
        if 'user_id' in session:
            return redirect(url_for('dashboard'))
        elif 'doctor_id' in session:
            return redirect(url_for('doctor_dashboard'))

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

    # --- DOKTOR SAYFALARI (YENİ) ---
    @app.route('/doctor_login', methods=['POST'])
    def doctor_login():
        email = request.form.get('email')
        password = request.form.get('password')
        doctor = Doctor.query.filter_by(email=email).first()
        
        if doctor and check_password_hash(doctor.password, password):
            session['doctor_id'] = doctor.id
            session['doctor_name'] = doctor.name
            return redirect(url_for('doctor_dashboard'))
        else:
            flash('Hatalı doktor e-postası veya şifre!', 'danger')
            return redirect(url_for('index'))

    @app.route('/doctor_dashboard')
    def doctor_dashboard():
        if 'doctor_id' not in session:
            return redirect(url_for('index'))
            
        appointments = Appointment.query.filter_by(doctor_id=session['doctor_id']).all()
        return render_template('doctor_dashboard.html', appointments=appointments, doctor_name=session['doctor_name'])

    # --- ORTAK ÇIKIŞ ---
    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('index'))

    return app