from flask import Flask, render_template, redirect, url_for, request
from apis.mascotas import mascotas_api
from apis.comentarios import comentarios_api
from apis.usuarios import usuarios_api

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/galeria')
def galeria():
    return render_template("galeria.html")

@app.route('/perfil/<int:id>')
def perfil_mascota(id):
    return render_template("perfilMascota.html", id=id)

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
