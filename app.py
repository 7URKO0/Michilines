from flask import Flask, Blueprint, request, jsonify, render_template, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Blueprint('api', __name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://powpatrol:Powpatrol1.@192.168.0.8/pawbase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Mascota(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    imagen_url = db.Column(db.String(200), nullable=True)
    edad = db.Column(db.String(50), nullable=True)
    raza = db.Column(db.String(50), nullable=True)
    zona = db.Column(db.String(50), nullable=True)
    estado = db.Column(db.String(50), nullable=True)
    comentarios = db.relationship('Comentario', backref='mascota', lazy=True)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    contrasena = db.Column(db.String(200), nullable=False)

class Comentario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contenido = db.Column(db.Text, nullable=False)
    mascota_id = db.Column(db.Integer, db.ForeignKey('mascota.id'), nullable=False)

@api.route('/mascotas/<int:id>', methods=['DELETE'])
def eliminar_mascota(id):
    mascota = Mascota.query.get_or_404(id)
    db.session.delete(mascota)
    db.session.commit()
    return jsonify({"mensaje": "Mascota eliminada exitosamente"}), 200

@api.route('/mascotas', methods=['GET'])
def obtener_mascotas():
    mascotas = Mascota.query.all()
    return jsonify([{
        "id": m.id,
        "nombre": m.nombre,
        "descripcion": m.descripcion,
        "imagen_url": m.imagen_url,
        "edad": m.edad,
        "raza": m.raza,
        "zona": m.zona,
        "estado": m.estado,
        "comentarios": m.comentarios
    } for m in mascotas])

@api.route('/mascotas', methods=['POST'])
def crear_mascota():
    data = request.json

    if not data or not all(key in data for key in ['nombre', 'descripcion', 'imagen_url', 'edad', 'raza', 'zona', 'estado']):
        return jsonify({"error": "Faltan campos obligatorios"}), 400
    nueva_mascota = Mascota(
        nombre=data.get('nombre'),
        descripcion=data.get('descripcion'),
        imagen_url=data.get('imagen_url'),
        edad=data.get('edad'),
        raza=data.get('raza'),
        zona=data.get('zona'),
        estado=data.get('estado')
    )
    db.session.add(nueva_mascota)
    db.session.commit()
    return jsonify({"mensaje": "Mascota creada exitosamente"}), 201

@app.route("/")
def index():
    datosIntegrantes = {
        "1": {"nombre":"Camila Pratto", "descripcion":"Estudiante de la Facultad de Ingenieria de la UBA. Estudia la carrera de Informatica.", "imagenUrl":"imagenes/persona1.png"},
        "2": {"nombre":"Camila Anahi Wilverht Rohr", "descripcion":"Estudiante de la Facultad de Ingenieria de la UBA. Estudia la carrera de Informatica.", "imagenUrl":"imagenes/persona2.png"},
        "3": {"nombre": "Francisca Gaillard", "descripcion" : "Estudiante de la Facultad de Ingenieria de la UBA. Estudia la carrera de Informatica.", "imagenUrl":"imagenes/persona3.png"},
        "4": {"nombre": "Ignacio Cettour", "descripcion" : "Estudiante de la Facultad de Ingenieria de la UBA. Estudia la carrera de Informatica.", "imagenUrl":"imagenes/persona4.png"},
        "5": {"nombre": "Lara Ovejero", "descripcion" : "Estudiante de la Facultad de Ingenieria de la UBA. Estudia la carrera de Informatica.", "imagenUrl":"imagenes/persona5.png"},
        "6": {"nombre": "Matias Rigano", "descripcion" : "Estudiante de la Facultad de Ingenieria de la UBA. Estudia la carrera de Informatica.", "imagenUrl":"imagenes/persona6.png"},
        "7": {"nombre": "Victor Oliva", "descripcion" : "Estudiante de la Facultad de Ingenieria de la UBA. Estudia la carrera de Informatica.", "imagenUrl":"imagenes/persona7.png"},
        "8": {"nombre": "Leonel Chaves", "descripcion" : "Profesor en la UBA y corrector del proyecto.", "imagenUrl":"imagenes/persona8.png"}

    }
    return render_template("index.html", datosIntegrantes=datosIntegrantes)


@app.route('/galeria')
def galeria():
    mascotas = Mascota.query.all()
    mascotas_dict = {
        mascota.id: {
            "nombre": mascota.nombre,
            "descripcion": mascota.descripcion,
            "imagen_url": mascota.imagen_url or "default.png",
            "edad": mascota.edad,
            "raza": mascota.raza,
            "estado": mascota.estado,
        }
        for mascota in mascotas
    }

    return render_template("galeria.html", mascotas=mascotas_dict)


@app.route('/perfil/<int:id>', methods=['GET', 'POST'])
def perfil_mascota(id):
    mascota = Mascota.query.get_or_404(id)
    if request.method == 'POST':
        comentario_contenido = request.form.get('comentario')
        if comentario_contenido:
            nuevo_comentario = Comentario(contenido=comentario_contenido, mascota_id=mascota.id)
            db.session.add(nuevo_comentario)
            db.session.commit()
        return redirect(url_for('perfil_mascota', id=id))
    return render_template("perfilMascota.html", mascota=mascota)

@app.route('/publicarMascotas', methods=['GET', 'POST'])
def publicarMascotas():
    if request.method == 'POST':
        nombre = request.form.get('nombreMascota')
        edad = request.form.get('edadMascota')
        descripcion = request.form.get('descripcion')
        especie = request.form.get('especie')
        condicion = request.form.get('condicion')
        fecha_perdida = request.form.get('fechaPerdida')
        ubicacion = request.form.get('ubicacion')

        if not nombre or not descripcion or not ubicacion:
            return "Faltan campos obligatorios", 400
        nueva_mascota = Mascota(
            nombre=nombre,
            descripcion=descripcion,
            imagen_url="url_de_imagen_placeholder",
            edad=edad,
            raza=especie,
            zona=ubicacion,
            estado=condicion
        )
        db.session.add(nueva_mascota)
        db.session.commit()

        return redirect(url_for('galeria'))

    return render_template("publicarMascotas.html")


@app.route('/registrarse', methods=['GET', 'POST'])
def registrarse():
    if request.method == 'POST':
        confirmar_contrasenia = request.form.get('confirmarContraseña')
        if not confirmar_contrasenia:
            return "La contraseña no puede estar vacía", 400
        if len(confirmar_contrasenia) < 8:
            return "La contraseña debe tener al menos 8 caracteres", 400
        return redirect(url_for('iniciarSesion'))
    return render_template('registrarse.html')



@app.route('/iniciarSesion', methods=['GET', 'POST'])
def iniciarSesion():
    if request.method == 'POST':
        nombre_usuario = request.form.get('nombreUsuario')
        contrasena = request.form.get('contrasena')
        if not nombre_usuario or not contrasena:
            return "Debe completar todos los campos", 400
        usuario = Usuario.query.filter_by(nombre_usuario=nombre_usuario).first()
        if usuario and usuario.contrasena == contrasena:
            return f"Bienvenido, {usuario.nombre_usuario}!"
        else:
            return "Nombre de usuario o contraseña incorrectos", 401

    return render_template('iniciarSesion.html')


@app.route('/integrantes')
def integrantes():
    datosIntegrantes = {
        "1": {"nombre":"Camila Pratto", "descripcion":"Estudiante de la Facultad de Ingenieria de la UBA. Estudia la carrera de Informatica.", "imagenUrl":"imagenes/persona1.png"},
        "2": {"nombre":"Camila Anahi Wilverht Rohr", "descripcion":"Estudiante de la Facultad de Ingenieria de la UBA. Estudia la carrera de Informatica.", "imagenUrl":"imagenes/persona2.png"},
        "3": {"nombre": "Francisca Gaillard", "descripcion" : "Estudiante de la Facultad de Ingenieria de la UBA. Estudia la carrera de Informatica.", "imagenUrl":"imagenes/persona3.png"},
        "4": {"nombre": "Ignacio Cettour", "descripcion" : "Estudiante de la Facultad de Ingenieria de la UBA. Estudia la carrera de Informatica.", "imagenUrl":"imagenes/persona4.png"},
        "5": {"nombre": "Lara Ovejero", "descripcion" : "Estudiante de la Facultad de Ingenieria de la UBA. Estudia la carrera de Informatica.", "imagenUrl":"imagenes/persona5.png"},
        "6": {"nombre": "Matias Rigano", "descripcion" : "Estudiante de la Facultad de Ingenieria de la UBA. Estudia la carrera de Informatica.", "imagenUrl":"imagenes/persona6.png"},
        "7": {"nombre": "Victor Oliva", "descripcion" : "Estudiante de la Facultad de Ingenieria de la UBA. Estudia la carrera de Informatica.", "imagenUrl":"imagenes/persona7.png"},
        "8": {"nombre": "Leonel Chaves", "descripcion" : "Profesor en la UBA y corrector del proyecto.", "imagenUrl":"imagenes/persona8.png"}

    }
    return render_template("integrantes.html", datosIntegrantes= datosIntegrantes)
app.register_blueprint(api, url_prefix='/api')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  
    app.run(debug=True)
