from flask import Flask, render_template, redirect, url_for, request, jsonify
from apis.mascotas import mascotas_api, obtener_conexion
from apis.comentarios import comentarios_api
from apis.usuarios import usuarios_api
#form_blueprint = Blueprint('form', _name_, template_folder='BACKEND/apis')
#concectar con el publicarMascotas(formulario)

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

@app.route('/galeria')
def galeria():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM mascotas")
        mascotas = cursor.fetchall()
    conexion.close()
    
    return render_template("galeria.html", mascotas=mascotas)


@app.route('/perfilMascota/<int:id>')
def perfilMascota(id):
    return render_template("perfilMascota.html", id=id)

@app.route('/publicar', METHODS=['POST'])
def publicar():
    nombre=request.form.get('nombreMascota')
    descripcion=request.form.get('descripcion')
    imagen_url=request.form.get('')
    raza=request.form.get('especie')
    zona=request.form.get('')
    estado=request.form.get('condicion')
    
    data={
        "nombre":nombre,
        "descripcion":descripcion,
        "raza":raza,
        "estado":estado
    }
    api_url = "http://powpatrol:Powpatrol1./mascotas" 
    try:
        # Enviar datos a la API usando POST
        response = requests.post(api_url, json=data)

        # Manejar la respuesta de la API
        if response.status_code == 200:
            api_response = response.json()
            return jsonify({
                "status": "success",
                "message": "Datos enviados correctamente a la API.",
                "api_response": api_response
            })
        else:
            return jsonify({
                "status": "error",
                "message": f"Error al enviar datos a la API. Código de estado: {response.status_code}"
            }), response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({
            "status": "error",
            "message": f"Error al conectar con la API: {str(e)}"
        }), 500

@app.route('/publicarMascotas')
def publicarMascotas():
    return render_template("publicarMascotas.html")


@app.route('/registrarse')
def registrarse():
    return render_template("registrarse.html")

@app.route('/iniciarSesion')
def iniciarSesion():
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
