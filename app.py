from flask import Flask, Blueprint, request, jsonify, render_template, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:tu_contraseña@localhost/michilines'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


class Mascota(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    imagen_url = db.Column(db.String(200), nullable=False)
    edad = db.Column(db.String(50), nullable=False)
    raza = db.Column(db.String(50), nullable=False)
    zona = db.Column(db.String(50), nullable=False)
    estado = db.Column(db.String(50), nullable=False)
    comentarios = db.Column(db.PickleType, default=[])

class Comentario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contenido = db.Column(db.Text, nullable=False)
    mascota_id = db.Column(db.Integer, db.ForeignKey('mascota.id'), nullable=False)
    mascota = db.relationship('Mascota', backref='comentarios') 
    
with app.app_context():
    db.create_all()

def poblar_mascotas():
    mascotas = [
        {
            "nombre": "Tomi",
            "descripcion": "Perro juguetón",
            "imagen_url": "imagenes/Tomi.png",
            "edad": "6 años",
            "raza": "Border Collie",
            "zona": "Palermo",
            "estado": "Tránsito"
        },
        {
            "nombre": "Luna",
            "descripcion": "Gatita juguetona y cariñosa",
            "imagen_url": "imagenes/Luna.png",
            "edad": "2 años",
            "raza": "Siamesa",
            "zona": "Villa Urquiza",
            "estado": "Perdido"
        },
        {
            'nombre': 'Bobby',
            'descripcion': 'Perro enérgico y leal',
            'imagenUrl': 'imagenes/Bobby.png',
            'edad': '5 años',
            'raza': 'Golden Retriever',
            'zona': 'Villa crespo',
            'estado':'Encontrado'
        },
        {
            'nombre': 'copito',
            'descripcion': 'conejo amigable y dienton',
            'imagenUrl': 'imagenes/copito.png',
            'edad': '5 meses',
            'raza': 'conejo',
            'zona': 'Once',
            'estado':'Encontrado',
        },
        {
            'nombre': 'franklin',
            'descripcion': 'tortuga timida e incomprendida',
            'imagenUrl': 'imagenes/franklin.jpg',
            'edad': '15 años',
            'raza': 'tortuga',
            'zona': 'Tigre',
            'estado':'Perdido',
        },  
        {
            'nombre': 'Cheems',
            'descripcion': 'Mascota simpática y amigable',
            'imagenUrl': 'imagenes/Cheems.png',
            'edad': '3 años',
            'raza': 'Shiba Inu',
            'zona': 'Belgrano',
            'estado':'Transito'
        },  
        {
            'nombre': 'Mara',
            'descripcion': 'Perra tranquila',
            'imagenUrl': 'imagenes/Mara.png',
            'edad': '4 años',
            'raza': 'Pug',
            'zona': 'Recoleta',
            'estado': 'Perdido'
        }
    ]

    
    for m in mascotas:
        if not Mascota.query.filter_by(nombre=m["nombre"]).first():
            nueva_mascota = Mascota(**m)
            db.session.add(nueva_mascota)
    db.session.commit()

poblar_mascotas()

api = Blueprint('api', __name__)

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
    nueva_mascota = Mascota(
        nombre=data.get('nombre'),
        descripcion=data.get('descripcion'),
        imagen_url=data.get('imagen_url'),
        edad=data.get('edad'),
        raza=data.get('raza'),
        zona=data.get('zona'),
        estado=data.get('estado'),
        comentarios=[]
    )
    db.session.add(nueva_mascota)
    db.session.commit()
    return jsonify({"mensaje": "Mascota creada exitosamente"}), 201


app.register_blueprint(api, url_prefix='/api')


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/galeria')
def galeria():
    mascotas = Mascota.query.all()
    return render_template("galeria.html", mascotas=mascotas)

@app.route('/perfil/<int:id>', methods=['GET', 'POST'])
def perfil_mascota(id):
    mascota = Mascota.query.get_or_404(id)
    if request.method == 'POST':
        comentario = request.form.get('comentario')
        if comentario:
            mascota.comentarios.append(comentario)
            db.session.commit()
        return redirect(url_for('perfil_mascota', id=id))
    return render_template("perfilMascota.html", mascota=mascota)

@app.route('/publicarMascotas')
def publicar_mascotas():
    return render_template("publicarMascotas.html")

@app.route('/registrarse')
def registrarse():
    return render_template("registrarse.html")

@app.route('/iniciarSesion')
def iniciar_sesion():
    return render_template("iniciarSesion.html")

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
    return render_template("integrantes.html", datos_integrantes=datos_integrantes)

if __name__ == "__main__":
    app.run(debug=True)
