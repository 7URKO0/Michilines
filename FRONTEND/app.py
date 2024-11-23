from flask import Flask, render_template, redirect, url_for, request
from apis.mascotas import mascotas_api, obtener_conexion
from apis.comentarios import comentarios_api
from apis.usuarios import usuarios_api

app = Flask(__name__)

@app.route('/index')
def index():
    #Esto creo que usando apis se puede evitar hardcodear
    datosIntegrantes = {
        "1": {"nombre":"Camila Pratto", "descripcion":"Ingenieria en Informatica", "imagenUrl":"imagenes/persona1.png"},
        "2": {"nombre":"Camila Anahi Wilverht Rohr", "descripcion":"Ingenieria en Informatica", "imagenUrl":"imagenes/persona2.png"},
        "3": {"nombre": "Francisca Gaillard", "descripcion" : "Ingenieria en Informatica", "imagenUrl":"imagenes/persona3.png"},
        "4": {"nombre": "Ignacio Cettour", "descripcion" : "Ingenieria en Informatica", "imagenUrl":"imagenes/persona4.png"},
        "5": {"nombre": "Lara Ovejero", "descripcion" : "Ingenieria en Informatica", "imagenUrl":"imagenes/persona5.png"},
        "6": {"nombre": "Matias Rigano", "descripcion" : "Ingenieria en Informatica", "imagenUrl":"imagenes/persona6.png"},
        "7": {"nombre": "Victor Oliva", "descripcion" : "Ingenieria en Informatica", "imagenUrl":"imagenes/persona7.png"},
        "8": {"nombre": "Leonel Chaves", "descripcion" : "Profesor en la UBA y corrector del proyecto.", "imagenUrl":"imagenes/persona8.png"}

    }
    return render_template("index.html", datosIntegrantes=datosIntegrantes)

@app.route('/')
def base():
    return render_template("base.html")

import requests

@app.route('/galeria')
def galeria():
    # URL de tu API
    api_url = 'http://localhost:5000/api/mascotas/listar'
    try:
        # Realiza la solicitud GET a la API
        response = requests.get(api_url)
        # Verifica si la solicitud fue exitosa
        if response.status_code == 200:
            mascotas = response.json()  # Convierte la respuesta en JSON
        else:
            mascotas = []  # Si falla, retorna una lista vacía
    except requests.exceptions.RequestException as e:
        print(f"Error al consumir la API: {e}")
        mascotas = []

    return render_template("galeria.html", mascotas=mascotas)

    
    return render_template("galeria.html", mascotas=mascotas)


@app.route('/perfil/<int:id>')
def perfilMascota(id):
    api_url = f'http://localhost:5000/api/mascotas/{id}'
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            mascota = response.json()  # Detalles de la mascota
        else:
            mascota = None  # Mascota no encontrada
    except requests.exceptions.RequestException as e:
        print(f"Error al consumir la API: {e}")
        mascota = None

    return render_template("perfilMascota.html", mascota=mascota)


@app.route('/perfil/<int:id>', methods=['GET', 'POST'])
def perfilMascota(id):
    if request.method == 'POST':
        comentario = request.form.get('comentario')
        # Lógica para guardar el comentario
        api_url = f'http://localhost:5000/api/comentarios'
        data = {
            "mascota_id": id,
            "contenido": comentario
        }
        try:
            requests.post(api_url, json=data)
            mensaje = "Comentario publicado con éxito"
        except Exception as e:
            mensaje = f"Error al publicar el comentario: {str(e)}"

    # Lógica para obtener los detalles de la mascota
    api_url = f'http://localhost:5000/api/mascotas/{id}'
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            mascota = response.json()
        else:
            return render_template("404.html"), 404
    except Exception as e:
        return render_template("500.html", error=str(e)), 500

    return render_template("perfilmascota.html", mascota=mascota)



@app.route('/registrarse', methods=['GET', 'POST'])
def registrarse():
    if request.method == 'POST':
        # Capturar los datos del formulario
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        correo = request.form.get('correo')
        contraseña = request.form.get('contraseña')
        confirmar_contraseña = request.form.get('confirmarContraseña')

        # Validar contraseñas
        if contraseña != confirmar_contraseña:
            mensaje = "Las contraseñas no coinciden. Inténtalo de nuevo."
            return render_template('registrarse.html', mensaje=mensaje)

        # Enviar datos a la API
        data = {
            "nombre": nombre,
            "apellido": apellido,
            "correo": correo,
            "contraseña": contraseña
        }

        try:
            response = requests.post('http://localhost:5000/api/usuarios', json=data)
            if response.status_code == 201:
                return redirect(url_for('iniciarSesion'))  # Redirigir a iniciar sesión
            else:
                error_message = response.json().get('message', 'Error desconocido')
                return render_template('registrarse.html', mensaje=f"Error: {error_message}")
        except requests.exceptions.RequestException as e:
            return render_template('registrarse.html', mensaje=f"Error al conectar con la API: {str(e)}")

    return render_template('registrarse.html')


@app.route('/iniciarSesion', methods=['GET', 'POST'])
def iniciarSesion():
    if request.method == 'POST':
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        
        # Conexión con la API
        api_url = 'http://localhost:5000/api/usuarios/login'
        data = {
            "correo": correo,
            "contraseña": contraseña
        }
        try:
            response = requests.post(api_url, json=data)
            if response.status_code == 200:
                usuario = response.json()
                mensaje = f"Bienvenido, {usuario['nombre']}!"
            else:
                mensaje = "Credenciales incorrectas, por favor verifica."
        except requests.exceptions.RequestException as e:
            mensaje = f"Error de conexión con la API: {str(e)}"
        
        return render_template("iniciarSesion.html", mensaje=mensaje)

    return render_template("iniciarSesion.html")


@app.route('/integrantes')
def integrantes():
    datos_integrantes = {
        "1": {"nombre":"Camila Pratto", "descripcion":"Estudiante de la Facultad de Ingeniería de la UBA. Estudia la carrera de Informática.", "imagenUrl":"imagenes/persona1.png"},
        "2": {"nombre":"Camila Anahi Wilverht Rohr", "descripcion":"Estudiante de la Facultad de Ingeniería de la UBA. Estudia la carrera de Informática.", "imagenUrl":"imagenes/persona2.png"},
        "3": {"nombre": "Francisca Gaillard", "descripcion" : "Estudiante de la Facultad de Ingeniería de la UBA. Estudia la carrera de Informática.", "imagenUrl":"imagenes/persona3.png"},
        "4": {"nombre": "Ignacio Cettour", "descripcion" : "Estudiante de la Facultad de Ingeniería de la UBA. Estudia la carrera de Informática.", "imagenUrl":"imagenes/persona4.png"},
        "5": {"nombre": "Lara Ovejero", "descripcion" : "Estudiante de la Facultad de Ingeniería de la UBA. Estudia la carrera de Informática.", "imagenUrl":"imagenes/persona5.png"},
        "6": {"nombre": "Matias Rigano", "descripcion" : "Estudiante de la Facultad de Ingeniería de la UBA. Estudia la carrera de Informática.", "imagenUrl":"imagenes/persona6.png"},
        "7": {"nombre": "Victor Oliva", "descripcion" : "Estudiante de la Facultad de Ingeniería de la UBA. Estudia la carrera de Informática.", "imagenUrl":"imagenes/persona7.png"},
        "8": {"nombre": "Leonel Chaves", "descripcion" : "Profesor en la UBA y corrector del proyecto.", "imagenUrl":"imagenes/persona8.png"}
    }
    return render_template("integrantes.html", datos_integrantes=datos_integrantes)

app.register_blueprint(mascotas_api, url_prefix='/api/mascotas')
app.register_blueprint(comentarios_api, url_prefix='/api/comentarios')
app.register_blueprint(usuarios_api, url_prefix='/api/usuarios')

if __name__ == "__main__":
    app.run(debug=True)
