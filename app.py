from flask import Flask, render_template, request, redirect, url_for

app=Flask(__name__)

@app.route('/')
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
    return render_template("galeria.html")

@app.route('/iniciarSesion')
def iniciarSesion():
    return render_template("iniciarSesion.html")

@app.route('/perfilMascota')
def perfilMascota():
    return render_template("perfilMascota.html")

@app.route('/publicarMascotas')
def publicarMascotas():
    return render_template("publicarMascotas.html")

@app.route('/registrarse')
def registrarse():
    return render_template("registrarse.html")

@app.route('/integrantes')
def integrantes():
    #Esto creo que usando apis se puede evitar hardcodear
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


if __name__ == "__main__":
    app.run(debug=True)