from flask import Flask, render_template
import os
from dotenv import load_dotenv
from .db.session import db

load_dotenv()

def create_app():
    app = Flask(__name__, template_folder='../templates')
    
    # SQLite yerine MariaDB bağlantımız. Kullanıcı: user, Şifre: 1234
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:1234@localhost/mhrs_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        from .routes.auth_routes import auth_bp
        from .routes.apt_routes import apt_bp
        app.register_blueprint(auth_bp, url_prefix='/auth')
        app.register_blueprint(apt_bp, url_prefix='/appointments')
        
        # Bu satır, MariaDB içinde user ve appointment tablolarını otomatik oluşturacak
        db.create_all() 

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/patient_panel/<int:id>')
    def patient_panel(id):
        return render_template('patient.html')

    return app