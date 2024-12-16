from src import crear_app, db  # Importa db y crear_app desde src
from src.models import User  # Importa el modelo User
from src.routes import users_bp # Importa el Blueprint de las rutas de usuarios


# Crear la aplicación
app = crear_app()
app.register_blueprint(users_bp, url_prefix='/users', name='pepe')

# Crear las tablas en la base de datos
with app.app_context():
    db.create_all()

# Iniciar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
