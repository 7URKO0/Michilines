from flask import Flask, render_template, request, redirect, url_for

app=Flask(__name__)

mascotas = {
    1: {
        'nombre': 'Cheems',
        'descripcion': 'Mascota simpática y amigable',
        'imagenUrl': 'imagenes/Cheems.jpg',
        'edad': '3 años',
        'raza': 'Shiba Inu',
        'zona': 'Belgrano'
    },
    2: {
        'nombre': 'Bobby',
        'descripcion': 'Perro enérgico y leal',
        'imagenUrl': 'imagenes/Bobby.jpg',
        'edad': '5 años',
        'raza': 'Golden Retriever',
        'zona': 'Villa crespo'
    },
    3: {
        'nombre': 'Luna',
        'descripcion': 'Gatita juguetona y cariñosa',
        'imagenUrl': 'imagenes/Luna.jpg',
        'edad': '2 años',
        'raza': 'Siamesa',
        'zona': 'Villa Urquiza'
    },
    4: {
        'nombre': 'copito',
        'descripcion': 'conejo amigable y dienton',
        'imagenUrl': 'imagenes/copito.jpg',
        'edad': '5 meses',
        'raza': 'conejo',
        'zona': 'Once'
    },
    5: {
        'nombre': 'franklin',
        'descripcion': 'tortuga timida e incomprendida',
        'imagenUrl': 'imagenes/copitofranklin.jpg',
        'edad': '15 años',
        'raza': 'tortuga',
        'zona': 'Tigre'
    },  
    6: {
        'nombre': 'Tomi',
        'descripcion': 'Perro jugueton',
        'imagenUrl': 'imagenes/Tomi.jpg',
        'edad': '6 años',
        'raza': 'Border Collie',
        'zona': 'Palermo'
    },  
    7: {
        'nombre': 'Mara',
        'descripcion': 'Perra tranquila',
        'imagenUrl': 'imagenes/Mara.jpg',
        'edad': '4 años',
        'raza': 'Pug',
        'zona': 'Recoleta'
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

@app.route('/perfil/<int:id>')
def perfilMascota(id):
    mascota = mascotas.get(id)
    if mascota:
        return render_template('perfilmascota.html', mascota=mascota)
    else:
        abort(404)


@app.route('/publicarMascotas')
def publicarMascotas():
    return render_template("publicarMascotas.html")

@app.route('/registrarse')
def registrarse():
    return render_template("registrarse.html")



if __name__ == "__main__":
    app.run(debug=True)