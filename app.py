from flask import Flask, render_template, request, redirect, url_for

app=Flask(__name__)

@app.route('/home')
def home():
    return render_template("home.html")

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



if __name__ == "__main__":
    app.run(debug=True)