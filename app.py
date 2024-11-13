from flask import Flask, render_template, request, redirect, url_for

app=Flask(__name__)

mascotas = {
    1: {
        'nombre': 'Tomi',
        'descripcion': 'Perro jugueton',
        'imagenUrl': 'imagenes/Tomi.png',
        'edad': '6 años',
        'raza': 'Border Collie',
        'zona': 'Palermo',
        'estado': 'Transito',
        'comentarios': []
    },
    2: {
        'nombre': 'Bobby',
        'descripcion': 'Perro enérgico y leal',
        'imagenUrl': 'imagenes/Bobby.png',
        'edad': '5 años',
        'raza': 'Golden Retriever',
        'zona': 'Villa crespo',
        'estado':'Encontrado',
        'comentarios': []
    },
    3: {
        'nombre': 'Luna',
        'descripcion': 'Gatita juguetona y cariñosa',
        'imagenUrl': 'imagenes/Luna.png',
        'edad': '2 años',
        'raza': 'Siamesa',
        'zona': 'Villa Urquiza',
        'estado': 'Perdido',
        'comentarios': []
    },
    4: {
        'nombre': 'copito',
        'descripcion': 'conejo amigable y dienton',
        'imagenUrl': 'imagenes/copito.png',
        'edad': '5 meses',
        'raza': 'conejo',
        'zona': 'Once',
        'estado':'Encontrado',
        'comentarios': []
    },
    5: {
        'nombre': 'franklin',
        'descripcion': 'tortuga timida e incomprendida',
        'imagenUrl': 'imagenes/franklin.jpg',
        'edad': '15 años',
        'raza': 'tortuga',
        'zona': 'Tigre',
        'estado':'Perdido',
        'comentarios': []

    },  
    6: {
        'nombre': 'Cheems',
        'descripcion': 'Mascota simpática y amigable',
        'imagenUrl': 'imagenes/Cheems.png',
        'edad': '3 años',
        'raza': 'Shiba Inu',
        'zona': 'Belgrano',
        'estado':'Transito',
        'comentarios': []
    },  
    7: {
        'nombre': 'Mara',
        'descripcion': 'Perra tranquila',
        'imagenUrl': 'imagenes/Mara.png',
        'edad': '4 años',
        'raza': 'Pug',
        'zona': 'Recoleta',
        'estado': 'Perdido',
        'comentarios': []
    },  
}


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
    return render_template("galeria.html", mascotas=mascotas)

@app.route('/iniciarSesion')
def iniciarSesion():
    return render_template("iniciarSesion.html")

@app.route('/perfil/<int:id>', methods=['GET', 'POST'])
def perfilMascota(id):
    mascota = mascotas.get(id)
    if not mascota:
        abort(404)
    if request.method == 'POST':
        comentario = request.form.get('comentario')
        if comentario:
            mascota['comentarios'].append(comentario)  
        return redirect(url_for('perfilMascota', id=id)) 

    return render_template('perfilMascota.html', mascota=mascota, id=id)


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