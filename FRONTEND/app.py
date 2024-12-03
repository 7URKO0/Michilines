from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from flask_bcrypt import Bcrypt
from datetime import datetime
import requests
from flask_cors import CORS
from pymysql.cursors import DictCursor

app = Flask(__name__)
app.secret_key = 'clave-super-secreta'  # Misma clave que en el backend
app.config['SESSION_COOKIE_DOMAIN'] = '127.0.0.1'
app.config['SESSION_COOKIE_SECURE'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB
CORS(app)
bcrypt = Bcrypt(app)
CORS(app, supports_credentials=True)
CORS(app)


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        port=3307,
        user="powpatrol",
        password="Powpatrol1.",
        database="pawbase"
    )

db_config = {
    "host": "localhost",
    "port": 3307,
    "user": "powpatrol",
    "password": "Powpatrol1.",
    "database": "pawbase"
}

# RUTA: Página principal
@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/integrantes')
def integrantes():
    datosIntegrantes = [
        {"nombre": "Camila Pratto", "descripcion": "Ingeniería en Informática", "imagenUrl": "imagenes/persona1.png"},
        {"nombre": "Camila Anahi Wilverht Rohr", "descripcion": "Ingeniería en Informática", "imagenUrl": "imagenes/persona2.png"},
        {"nombre": "Francisca Gaillard", "descripcion": "Ingeniería en Informática", "imagenUrl": "imagenes/persona3.png"},
        {"nombre": "Ignacio Cettour", "descripcion": "Ingeniería en Informática", "imagenUrl": "imagenes/persona4.png"},
        {"nombre": "Lara Ovejero", "descripcion": "Ingeniería en Informática", "imagenUrl": "imagenes/persona5.png"},
        {"nombre": "Matias Rigano", "descripcion": "Ingeniería en Informática", "imagenUrl": "imagenes/persona6.png"},
        {"nombre": "Victor Oliva", "descripcion": "Ingeniería en Informática", "imagenUrl": "imagenes/persona7.png"},
        {"nombre": "Leonel Chaves", "descripcion": "Profesor en la UBA y corrector del proyecto.", "imagenUrl": "imagenes/leo.jpg"},
    ]
    return render_template("integrantes.html", datosIntegrantes=datosIntegrantes)

@app.route('/galeria', methods=['GET'])
def galeria():
    try:
        response = requests.get('http://127.0.0.1:5001/mascotas')
        if response.status_code == 200:
            mascotas = response.json()
            return render_template('galeria.html', mascotas=mascotas)
        elif response.status_code == 404:
            return render_template('galeria.html', mascotas=[], error="No se encontraron mascotas.")
        else:
            print(f"Error del backend: {response.status_code} - {response.text}")
            return render_template('galeria.html', mascotas=[], error="Hubo un problema al cargar la galería.")
    except Exception as e:
        print(f"Error en galeria: {str(e)}")
        return render_template('galeria.html', mascotas=[], error="No se pudo conectar con el backend.")

@app.route('/perfil/<int:id>', methods=['GET', 'POST'])
def perfilMascota(id):
    try:
        print("Sesión actual:", dict(session))

        # Verifica si el usuario está autenticado
        if 'id_usuarios' not in session:
            return redirect(url_for('iniciarSesion'))

        # Obtener datos de la mascota (incluye foto en Base64 y coordenadas)
        response_mascota = requests.get(f'http://127.0.0.1:5001/mascotas/{id}')
        if response_mascota.status_code == 200:
            mascota = response_mascota.json()

            # Validar que la mascota tenga coordenadas válidas
            if not mascota.get('latitud') or not mascota.get('longitud'):
                print(f"Error: Mascota con ID {id} no tiene coordenadas válidas.")
                mascota['latitud'] = None
                mascota['longitud'] = None
        else:
            return render_template("404.html"), 404

        # Obtener comentarios de la mascota
        response_comentarios = requests.get(f'http://127.0.0.1:5001/mascotas/{id}/comentarios')
        comentarios = response_comentarios.json() if response_comentarios.status_code == 200 else []

        # Manejar envío de nuevos comentarios
        if request.method == 'POST':
            comentario_texto = request.form.get('comentario')
            if not comentario_texto:
                error = "El comentario no puede estar vacío."
                return render_template("perfilMascota.html", 
                                       mascota=mascota, 
                                       comentarios=comentarios, 
                                       id=id, 
                                       error=error)
            
            nuevo_comentario = {
                "id_mascota": id,
                "id_usuario": session.get('id_usuarios', None),
                "texto": comentario_texto
            }
            response_post = requests.post('http://127.0.0.1:5001/comentarios', json=nuevo_comentario)
            if response_post.status_code == 201:
                return redirect(url_for('perfilMascota', id=id))
            else:
                error = "Error al guardar el comentario."
                return render_template("perfilMascota.html", 
                                       mascota=mascota, 
                                       comentarios=comentarios, 
                                       id=id, 
                                       error=error)

        # Renderizar el template con los datos de la mascota, incluyendo coordenadas
        return render_template("perfilMascota.html", 
                               mascota=mascota, 
                               comentarios=comentarios, 
                               id=id, 
                               session=dict(session))
    except Exception as e:
        print(f"Error en perfilMascota: {str(e)}")
        return f"Error al cargar el perfil de la mascota: {str(e)}", 500



# RUTA: Publicar una mascota perdida
@app.route('/publicarMascotas', methods=['GET'])
def publicarMascotas():
    return render_template('publicarMascotas.html')


@app.route('/registrarse', methods=['GET'])
def registrarse():
    return render_template('registrarse.html')

# RUTA: Iniciar sesión
@app.route('/iniciarSesion', methods=['GET'])
def iniciarSesion():
    return render_template('iniciarSesion.html')

if __name__ == "__main__":
    app.run(debug=True, port=3609)

