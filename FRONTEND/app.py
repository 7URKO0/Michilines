from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from datetime import datetime

app = Flask(__name__)


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        port=3307,
        user="powpatrol",
        password="Powpatrol1.",
        database="pawbase"
    )
# Configuración de la conexión a la base de datos
db_config = {
    'host': 'localhost',
    'user': 'root',  # Cambia esto por tu usuario de MySQL
    'password': 'tu_contraseña',  # Cambia esto por tu contraseña
    'database': 'michilines'  # Cambia esto por el nombre de tu base de datos
}

# RUTA: Página principal
@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/integrantes')
def integrantes():
    datos_integrantes = [
        {"nombre": "Camila Pratto", "descripcion": "Ingeniería en Informática", "imagenUrl": "imagenes/persona1.png"},
        {"nombre": "Camila Anahi Wilverht Rohr", "descripcion": "Ingeniería en Informática", "imagenUrl": "imagenes/persona2.png"},
        {"nombre": "Francisca Gaillard", "descripcion": "Ingeniería en Informática", "imagenUrl": "imagenes/persona3.png"},
        {"nombre": "Ignacio Cettour", "descripcion": "Ingeniería en Informática", "imagenUrl": "imagenes/persona4.png"},
        {"nombre": "Lara Ovejero", "descripcion": "Ingeniería en Informática", "imagenUrl": "imagenes/persona5.png"},
        {"nombre": "Matias Rigano", "descripcion": "Ingeniería en Informática", "imagenUrl": "imagenes/persona6.png"},
        {"nombre": "Victor Oliva", "descripcion": "Ingeniería en Informática", "imagenUrl": "imagenes/persona7.png"},
        {"nombre": "Leonel Chaves", "descripcion": "Profesor en la UBA y corrector del proyecto.", "imagenUrl": "imagenes/persona8.png"},
    ]
    return render_template("integrantes.html", datos_integrantes=datos_integrantes)

@app.route('/galeria', methods=['GET'])
def galeria():
    connection = None
    cursor = None
    try:
        # Conecta a la base de datos
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        # Consulta para obtener las mascotas
        query = "SELECT * FROM mascotas"
        cursor.execute(query)
        mascotas = cursor.fetchall()

        return render_template("galeria.html", mascotas=mascotas)

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "Error al cargar la galería.", 500

    finally:
        # Cierra el cursor y la conexión si fueron inicializados
        if cursor:
            cursor.close()
        if connection:
            connection.close()



# RUTA: Perfil de mascota
@app.route('/perfil/<int:id>', methods=['GET'])
def perfilMascota(id):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM mascotas WHERE id = %s"
        cursor.execute(query, (id,))
        mascota = cursor.fetchone()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        mascota = None
    finally:
        cursor.close()
        connection.close()

    if mascota:
        return render_template("perfilMascota.html", mascota=mascota)
    else:
        return render_template("404.html"), 404

# RUTA: Publicar una mascota perdida
@app.route('/publicarMascotas', methods=['GET', 'POST'])
def publicarMascotas():
    if request.method == 'POST':
        # Captura datos del formulario
        id_usuario = 1  # Cambia esto para usar el ID del usuario autenticado
        nombre = request.form.get('nombre')
        tipo = request.form.get('especie')
        estado = request.form.get('condicion')
        descripcion = request.form.get('descripcion')
        zona = request.form.get('zona', 'No especificada')  # Agrega 'zona' si la tienes en el formulario
        fecha_perdida = request.form.get('fecha_perdida')
        comentario = request.form.get('comentario', None)

        # Procesar la foto como BLOB
        foto = request.files.get('foto')
        foto_blob = foto.read() if foto else None

        # Inicializa las variables para el cursor y la conexión
        connection = None
        cursor = None

        try:
            # Conecta a la base de datos
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()

            # Insertar datos en la tabla `mascotas`
            query = """
                INSERT INTO mascotas (id_usuarios, nombre, tipo, estado, descripcion, foto, zona, fecha_publicacion, comentario)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                id_usuario, nombre, tipo, estado, descripcion, foto_blob, zona, fecha_perdida, comentario
            ))
            connection.commit()
            mensaje = "La mascota se ha publicado con éxito."
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            mensaje = "Ocurrió un error al publicar la mascota. Intenta de nuevo."
        finally:
            # Cierra el cursor y la conexión si fueron inicializados
            if cursor:
                cursor.close()
            if connection:
                connection.close()

        return render_template("publicarMascotas.html", mensaje=mensaje)

    # Si es una solicitud GET, renderiza el formulario
    return render_template('publicarMascotas.html')


# RUTA: Registro de usuarios
@app.route('/registrarse', methods=['GET', 'POST'])
def registrarse():
    if request.method == 'POST':
        # Capturar datos del formulario
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        correo = request.form.get('correo')
        contraseña = request.form.get('contraseña')
        confirmar_contraseña = request.form.get('confirmarContraseña')

        # Validar contraseñas
        if contraseña != confirmar_contraseña:
            mensaje = "Las contraseñas no coinciden. Inténtalo de nuevo."
            return render_template('registrarse.html', mensaje=mensaje)

        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()
            query = """
                INSERT INTO usuarios (nombre, apellido, correo, contraseña)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (nombre, apellido, correo, contraseña))
            connection.commit()
            return redirect(url_for('iniciarSesion'))
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            mensaje = "Ocurrió un error al registrar el usuario. Intenta de nuevo."
        finally:
            cursor.close()
            connection.close()

    return render_template('registrarse.html')

# RUTA: Iniciar sesión
@app.route('/iniciarSesion', methods=['GET', 'POST'])
def iniciarSesion():
    if request.method == 'POST':
        correo = request.form.get('correo')
        contraseña = request.form.get('contraseña')

        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM usuarios WHERE correo = %s AND contraseña = %s"
            cursor.execute(query, (correo, contraseña))
            usuario = cursor.fetchone()

            if usuario:
                mensaje = f"Bienvenido, {usuario['nombre']}!"
                return redirect(url_for('index'))
            else:
                mensaje = "Credenciales incorrectas. Intenta de nuevo."
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            mensaje = "Error al conectar con la base de datos. Intenta de nuevo."
        finally:
            cursor.close()
            connection.close()

        return render_template("iniciarSesion.html", mensaje=mensaje)

    return render_template("iniciarSesion.html")

if __name__ == "__main__":
    app.run(debug=True, port=3608)

