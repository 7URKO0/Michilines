from flask import Flask, render_template, request, redirect, url_for

app=Flask(__name__)

mascotas = {
    1: {
        'nombre': 'Tomi',
        'descripcion': 'Perro jugueton',
        'imagenUrl': 'imagenes/Tomi.jpg',
        'edad': '6 años',
        'raza': 'Border Collie',
        'zona': 'Palermo',
        'estado': 'Transito',
        'comentarios': []
    },
    2: {
        'nombre': 'Bobby',
        'descripcion': 'Perro enérgico y leal',
        'imagenUrl': 'imagenes/Bobby.jpg',
        'edad': '5 años',
        'raza': 'Golden Retriever',
        'zona': 'Villa crespo',
        'estado':'Encontrado',
        'comentarios': []
    },
    3: {
        'nombre': 'Luna',
        'descripcion': 'Gatita juguetona y cariñosa',
        'imagenUrl': 'imagenes/Luna.jpg',
        'edad': '2 años',
        'raza': 'Siamesa',
        'zona': 'Villa Urquiza',
        'estado': 'Perdido',
        'comentarios': []
    },
    4: {
        'nombre': 'copito',
        'descripcion': 'conejo amigable y dienton',
        'imagenUrl': 'imagenes/copito.jpg',
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
        'imagenUrl': 'imagenes/Cheems.jpg',
        'edad': '3 años',
        'raza': 'Shiba Inu',
        'zona': 'Belgrano',
        'estado':'Transito',
        'comentarios': []
    },  
    7: {
        'nombre': 'Mara',
        'descripcion': 'Perra tranquila',
        'imagenUrl': 'imagenes/Mara.jpg',
        'edad': '4 años',
        'raza': 'Pug',
        'zona': 'Recoleta',
        'estado': 'Perdido',
        'comentarios': []
    },  
}


@app.route('/')
def index():
    return render_template("index.html")

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

    return render_template('perfilmascota.html', mascota=mascota, id=id)



@app.route('/publicarMascotas')
def publicarMascotas():
    return render_template("publicarMascotas.html")

@app.route('/registrarse')
def registrarse():
    return render_template("registrarse.html")



if __name__ == "__main__":
    app.run(debug=True)