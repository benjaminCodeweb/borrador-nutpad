from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config
import os

db: SQLAlchemy = SQLAlchemy()
migrate: Migrate  = Migrate()


def crear_app() -> Flask:
    app =  Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SECRET_KEY'] = os.urandom(32) 
    db.init_app(app= app)
    app.app_context().push()
    
    from  src.routes import users_bp 

    app.register_blueprint(blueprint=users_bp)
    return app 