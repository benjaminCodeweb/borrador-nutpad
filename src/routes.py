from flask import Blueprint, render_template, request, jsonify, url_for, redirect, flash, session, json
from typing import Tuple, Any
from flask_login import current_user 
from src.models import User, db  # Importa después de definir db
from flask_sqlalchemy import SQLAlchemy
from src.models import Programa, Planss
from src.schemas import UserCreateSchema

users_bp = Blueprint('users', __name__)

@users_bp.route('/')
def index():
    return render_template('index.html')

@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        data = request.form
        if User.query.filter_by(username=data['username']).first():
             flash("el nombre de usuario ya existe")
             return render_template('register.html')
        
        user = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            username=data['username'],
            age=int(data['age']),
            weight=float(data['weight'])
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        return redirect('/login') 


@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    elif request.method == 'POST':
        data = request.form
        user = User.query.filter_by(username=data['username']).first()
        
        if user and user.check_password(data['password']):
            session['user_id'] = user.id  # Guarda el ID del usuario en la sesión
            return redirect(url_for('users.programa_nutricional'))
        else:
            flash('Nombre de usuario o contraseña incorrectos.', 'error')
            return render_template('login.html')
@users_bp.route('/users', methods=['POST'])
def create_user() -> str:
    data: Tuple[Any] = request.form

    try: 
        user_data = UserCreateSchema(first_name = data['first_name'], last_name = data ['last_name'], username = data['username'], edad = data['edad'], altura = data['altura'] )


    except  ValueError as e:
        return jsonify({"error": e}), 400
    
    new_user: User =  User(first_name = data['first_name'], last_name = data ['last_name'], username = data['username'], edad = data['edad'], altura = data['altura'] )

    db.session.add(new_user) 
    db.session.commit()

    return render_template('programa_nutricional.html', user= new_user)


@users_bp.route('/programa', methods=['POST'], endpoint="programa")
def guardar_programa():
    datos = request.form
    try:
        # Crear una nueva instancia de Programa
        nuevo_programa = Programa(
            edad=datos['edad'],
            altura=datos['altura'],
            peso=datos['peso'],
            sexo=datos['sexo'],
            actividad=datos['actividad'],
            objetivo=datos['objetivo'],
            condiciones_medicas=datos.get('condiciones_medicas', ''),
            alergias=datos.get('alergias', ''),
            preferencias=datos.get('preferencias', ''),
            horario_comidas=datos.get('horario_comidas', ''),
            hidratacion=datos.get('hidratacion', 0),
            consumo_alimentos=datos.get('consumo_alimentos', ''),
            historial_peso=datos.get('historial_peso', ''),
            estres_sueño=datos.get('estres_sueño', ''),
            restricciones_culturales=datos.get('restricciones_culturales', '')
        )
        # Guardar en la base de datos
        db.session.add(nuevo_programa)
        db.session.commit()
     
        flash("Datos guardados correctamente")
        return render_template('programa_nutricional.html', plan = nuevo_programa) # Cambia 'users.index' al endpoint que prefieras
    
    except Exception as e:
          # Manejar errores y mostrar un mensaje
         db.session.rollback()
         flash(f"Error al guardar datos: {str(e)}")
         return render_template('programa.html')
    
def generate_weekly_plan(objetivo):
    if objetivo == 'perder_peso':
        return {
            "lunes": ["Avena con frutas", "Ensalada de pollo", "Pescado al vapor con verduras"],
            "martes": ["Tostadas integrales con aguacate", "Pechuga de pollo con arroz integral", "Sopa de lentejas"],
            "miercoles": ["Batido de proteínas con plátano", "Ensalada de atún", "Tacos de lechuga con carne magra"],
            "jueves": ["Yogur griego con granola", "Pavo con quinoa y espárragos", "Pescado a la parrilla con brócoli"],
            "viernes": ["Huevos revueltos con espinacas", "Pollo al horno con camote", "Sopa de vegetales"],
            "sabado": ["Smoothie verde", "Arroz con vegetales y pollo", "Ensalada de garbanzos"],
            "domingo": ["Tostadas con aguacate", "Pasta integral con atún", "Salmón con espárragos"]
        }
    elif objetivo == 'ganar_musculo':
        return {
            "lunes": ["Huevos con pan integral", "Arroz con pollo y aguacate", "Carne magra con batata"],
            "martes": ["Batido de proteínas", "Pasta integral con carne molida", "Pollo al curry con arroz"],
            "miercoles": ["Panqueques de avena", "Salmón con quinoa", "Ensalada de pollo y garbanzos"],
            "jueves": ["Avena con mantequilla de maní", "Carne de res con papa y espárragos", "Pechuga de pollo con arroz"],
            "viernes": ["Tostadas con aguacate y huevo", "Hamburguesa de pavo casera", "Salmón a la parrilla con puré de papas"],
            "sabado": ["Tacos de carne magra", "Pollo al horno con vegetales", "Arroz con salmón"],
            "domingo": ["Tostadas integrales con huevo", "Ensalada César con pollo", "Pasta con carne magra"]
        }
    elif objetivo == 'mantener_peso':
        return {
            "lunes": ["Tostadas con aguacate", "Ensalada César con pollo", "Pescado al horno con espárragos"],
            "martes": ["Yogur con frutas y nueces", "Pechuga de pollo con arroz integral", "Carne magra con puré de camote"],
            "miercoles": ["Pan integral con mantequilla de almendras", "Salmón con ensalada verde", "Sopa de lentejas"],
            "jueves": ["Huevos duros y tostadas", "Pasta integral con pollo", "Ensalada de atún con garbanzos"],
            "viernes": ["Batido de frutas y yogur", "Arroz con carne molida y vegetales", "Pollo al horno con espinacas"],
            "sabado": ["Smoothie de frutas", "Carne a la parrilla con puré", "Sopa de vegetales"],
            "domingo": ["Pancakes integrales", "Quinoa con pollo", "Ensalada de salmón"]
        }
    elif objetivo == 'mejorar_salud':
        return {
            "lunes": ["Tostada con aguacate", "Ensalada César con pollo", "Pescado al horno con espárragos"],
            "martes": ["Yogur con frutas y nueces", "Pechuga de pollo con arroz integral", "Carne magra con puré de camote"],
            "miercoles": ["Pan integral con mantequilla de almendras", "Salmón con ensalada verde", "Sopa de lentejas"],
            "jueves": ["Huevos duros y tostadas", "Pasta integral con pollo", "Ensalada de atún con garbanzos"],
            "viernes": ["Batido de frutas y yogur", "Arroz con carne molida y vegetales", "Pollo al horno con espinacas"],
            "sabado": ["Smoothie de frutas", "Carne a la parrilla con puré", "Sopa de vegetales"],
            "domingo": ["Pancakes integrales", "Quinoa con pollo", "Ensalada de salmón"]
        }
    else:
        return {}

@users_bp.route('/programa_nutricional', endpoint='programa_nutricional', methods=['GET', 'POST'])
def generate_plan():
    # Obtener datos del formulario
    if request.method == 'POST': 
        nombre = request.form.get('name')
        objetivo = request.form.get('objetivo')
    
    # Generar el plan semanal usando la función
    weekly_plan = generate_weekly_plan(objetivo)
    
    if not weekly_plan:
        return render_template ('programa.html')
    
    # Guardar el plan en la base de datos
    weekly_plan_json = json.dumps(weekly_plan)  # Convertir a JSON para guardar
    new_plan = Planss(nombre=nombre, objetivo=objetivo, weekly_plan=weekly_plan_json)
    db.session.add(new_plan)
    db.session.commit()
    
    return render_template('programa_nutricional.html', nombre=nombre, weekly_plan=weekly_plan)


   

