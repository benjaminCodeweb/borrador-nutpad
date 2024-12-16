from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from src import db
from sqlalchemy import ForeignKey 
from sqlalchemy.orm import relationship 





class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    #posts = db.relationship('Programa', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class Programa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    altura = db.Column(db.Integer, nullable=False)
    peso = db.Column(db.Float, nullable=False)
    sexo = db.Column(db.String(10), nullable=False)
    actividad = db.Column(db.String(20), nullable=False)
    objetivo = db.Column(db.String(50), nullable=False)
    condiciones_medicas = db.Column(db.String(200), nullable=True)
    alergias = db.Column(db.String(200), nullable=True)
    preferencias = db.Column(db.String(200), nullable=True)
    horario_comidas = db.Column(db.String(200), nullable=True)
    hidratacion = db.Column(db.Float, nullable=True)
    consumo_alimentos = db.Column(db.String(200), nullable=True)
    historial_peso = db.Column(db.String(200), nullable=True)
    estres_sueño = db.Column(db.String(200), nullable=True)
    restricciones_culturales = db.Column(db.String(200), nullable=True)
    
    plans = db.relationship('Planss', backref='programa', lazy=True)

class Planss(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('programa.id'), nullable=False)
    monday = db.Column(db.String(500), nullable=False)
    tuesday = db.Column(db.String(500), nullable=False)
    wednesday = db.Column(db.String(500), nullable=False)
    thursday = db.Column(db.String(500), nullable=False)
    friday = db.Column(db.String(500), nullable=False)
    saturday = db.Column(db.String(500), nullable=False)
    sunday = db.Column(db.String(500), nullable=False)
    weekly_plan = db.Column(db.Text, nullable=False)  