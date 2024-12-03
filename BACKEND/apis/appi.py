from flask import Flask, jsonify, request, redirect, session
from flask_bcrypt import Bcrypt  # Solo Flask-Bcrypt
import pymysql.cursors
import base64
from pymysql.cursors import DictCursor
import requests
from flask_cors import CORS

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = 'clave-super-secreta' 
CORS(app, supports_credentials=True)
CORS(app)
app.config['SESSION_COOKIE_DOMAIN'] = '127.0.0.1'  # Configura para localhost
app.config['SESSION_COOKIE_SECURE'] = False        # Solo si no estás usando HTTPS

MAX_FILE_SIZE = 16 * 1024 * 1024  # 16 MB
# Configuración de la base de datos
db_config = {
    "host": "localhost",
    "port": 3307,
    "user": "powpatrol",
    "password": "Powpatrol1.",
    "database": "pawbase"
}
def get_db_connection():
    return pymysql.connect(
        host=db_config["host"],
        port=db_config["port"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["database"],
        cursorclass=pymysql.cursors.DictCursor
    )

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
# --- Rutas para Mascotas---
""" CAMBIOS """
@app.route('/mascotas', methods=['POST'])
def agregar_mascota():
    if 'id_usuarios' not in session:
        return jsonify({"auth": False, "message": "Usuario no autenticado"}), 401

    try:
        # Datos generales del formulario
        id_usuarios = session['id_usuarios']
        nombre = request.form.get('nombre')
        tipo = request.form.get('tipo')
        estado = request.form.get('estado')
        descripcion = request.form.get('descripcion')
        zona = request.form.get('zona', 'No especificada')

        # Coordenadas del formulario
        latitud = request.form.get('latitud')
        longitud = request.form.get('longitud')

        # Validar coordenadas
        if not latitud or not longitud:
            return jsonify({"message": "Por favor selecciona una ubicación en el mapa."}), 400

        # Verificar archivo recibido
        foto = request.files.get('foto')
        if foto:
            foto_bytes = foto.read()
            foto_base64 = base64.b64encode(foto_bytes).decode('utf-8')
        else:
            foto_base64 = None

        # Validar campos obligatorios
        if not all([nombre, tipo, estado, descripcion, latitud, longitud]):
            return jsonify({"message": "Faltan datos obligatorios"}), 400

        # Guardar en base de datos
        query = """
            INSERT INTO mascotas (id_usuarios, nombre, tipo, estado, descripcion, foto, zona, latitud, longitud, fecha_publicacion)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
        """
        valores = (id_usuarios, nombre, tipo, estado, descripcion, foto_base64, zona, latitud, longitud)
        
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(query, valores)
            connection.commit()

        return jsonify({"message": "Mascota publicada exitosamente"}), 201
    except Exception as e:
        print(f"Error en agregar_mascota: {str(e)}")
        return jsonify({"message": "Error al procesar la solicitud"}), 500




""" @app.route('/galeria/eliminar/<int:id>', methods=['POST'])
def eliminar_mascota(id):
    backend_url = f'http://127.0.0.1:5001/mascotas/{id}'

    try:
        # Realizar la solicitud DELETE al backend
        response = requests.delete(backend_url)

        if response.status_code == 200:
            print(f"Mascota con ID {id} eliminada exitosamente.")
            return jsonify({"message": "Mascota eliminada exitosamente"}), 200
        elif response.status_code == 404:
            print(f"Mascota con ID {id} no encontrada.")
            return jsonify({"message": "Mascota no encontrada"}), 404
        else:
            print(f"Error al eliminar la mascota: {response.status_code} - {response.text}")
            return jsonify({"message": "Error al eliminar la mascota."}), 500
    except Exception as e:
        print(f"Error en la conexión con el backend: {e}")
        return jsonify({"message": f"Error al conectar con el backend: {str(e)}"}), 500
 """



""" BIEN """
@app.route('/mascotas', methods=['GET'])
def obtener_mascotas():
    # Obtener filtros desde la URL
    tipo = request.args.get('tipo', None)
    estado = request.args.get('estado', None)

    # Construir la consulta con filtros dinámicos
    query = "SELECT id, nombre, tipo, estado, descripcion, zona, foto FROM mascotas WHERE 1=1"
    params = []

    if tipo:
        query += " AND tipo = %s"
        params.append(tipo)
    if estado:
        query += " AND estado = %s"
        params.append(estado)

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(query, tuple(params))
            resultado = cursor.fetchall()

            mascotas = []
            for row in resultado:
                mascota = {
                    'id': row['id'],
                    'nombre': row['nombre'],
                    'tipo': row['tipo'],
                    'estado': row['estado'],
                    'descripcion': row['descripcion'],
                    'zona': row['zona'],
                    'foto': row['foto']
                }
                mascotas.append(mascota)

            return jsonify(mascotas), 200
    except Exception as e:
        print(f"Error en obtener_mascotas: {e}")
        return jsonify({'message': f'Error al obtener mascotas: {str(e)}'}), 500
    finally:
        connection.close()





""" BIEN """
@app.route('/mascotas/<int:id>', methods=['GET'])
def obtener_perfil_mascota(id):
    query = "SELECT id, nombre, tipo, estado, descripcion, zona, foto, latitud, longitud FROM mascotas WHERE id = %s;"
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(query, (id,))
            resultado = cursor.fetchone()

            if resultado:
                # Verificar y manejar el campo foto correctamente
                if resultado['foto']:
                    if isinstance(resultado['foto'], bytes):  # Si es binario, codificar a Base64
                        foto = base64.b64encode(resultado['foto']).decode('utf-8')
                    else:
                        foto = resultado['foto']  # Si ya es un string, asumir que es Base64
                else:
                    foto = None
                latitud = float(resultado['latitud']) if resultado['latitud'] else None
                longitud = float(resultado['longitud']) if resultado['longitud'] else None
                mascota = {
                    "id": resultado['id'],
                    "nombre": resultado['nombre'],
                    "tipo": resultado['tipo'],
                    "estado": resultado['estado'],
                    "descripcion": resultado['descripcion'],
                    "zona": resultado['zona'],
                    "foto": foto,
                    "latitud": latitud,  # Incluye latitud
                    "longitud": longitud # Incluye longitud
                }
                return jsonify(mascota), 200
            else:
                return jsonify({'message': 'Mascota no encontrada'}), 404
    except Exception as e:
        print(f"Error en obtener_perfil_mascota: {e}")
        return jsonify({'message': f'Error al obtener perfil de la mascota: {str(e)}'}), 500
    finally:
        connection.close()



# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
# --- Rutas para Comentarios ---
""" BIEN """
@app.route('/mascotas/<int:id>/comentarios', methods=['GET'])
def obtener_comentarios(id):
    query = """
        SELECT c.texto AS comentario, u.nombre AS usuario
        FROM comentarios c
        JOIN usuarios u ON c.id_usuario = u.id_usuarios
        WHERE c.id_mascota = %s
        ORDER BY c.fecha_comentario DESC;
    """
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(query, (id,))
            comentarios = cursor.fetchall()
            return jsonify(comentarios or []), 200
    except Exception as e:
        print(f"Error en obtener_comentarios: {e}")
        return jsonify({'message': f'Error al obtener comentarios: {str(e)}'}), 500
    finally:
        connection.close()
""" BIEN """
@app.route('/comentarios', methods=['POST'])
def agregar_comentario():
    nuevo_comentario = request.get_json()

    if not all(k in nuevo_comentario for k in ('id_mascota', 'id_usuario', 'texto')):
        return jsonify({'message': 'Faltan datos obligatorios'}), 400

    query = """INSERT INTO comentarios (id_mascota, id_usuario, texto)
               VALUES (%s, %s, %s);"""
    values = (
        nuevo_comentario['id_mascota'], nuevo_comentario['id_usuario'], nuevo_comentario['texto']
    )
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(query, values)
            connection.commit()
        return jsonify({'message': 'Comentario agregado exitosamente'}), 201
    except Exception as e:
        print(f"Error en agregar_comentario: {e}")
        return jsonify({'message': f'Error al agregar comentario: {str(e)}'}), 500
    finally:
        connection.close()

    

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
# --- Rutas para Usuarios ---
""" BIEN """
@app.route('/usuarios', methods=['POST'])
def registrar_usuario():
    data = request.form.to_dict()  # Captura datos del formulario en formato clave-valor
    print("Datos recibidos:", data)  # Para depuración

    # Validación de campos requeridos
    campos_requeridos = ['nombre', 'apellido', 'correo', 'contrasni', 'confirmarContrasni']
    if not all(campo in data for campo in campos_requeridos):
        return jsonify({"message": "Faltan datos obligatorios"}), 400

    # Verificar que las contraseñas coincidan
    if data['contrasni'] != data['confirmarContrasni']:
        return jsonify({"message": "Las contraseñas no coinciden"}), 400

    # Hashear la contraseña
    hashed_password = bcrypt.generate_password_hash(data['contrasni']).decode('utf-8')

    query_insert = """
        INSERT INTO usuarios (nombre, apellido, correo, contrasni)
        VALUES (%s, %s, %s, %s)
    """
    query_check = "SELECT * FROM usuarios WHERE correo = %s"

    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Verificar si el correo ya está registrado
        cursor.execute(query_check, (data['correo'],))
        if cursor.fetchone():
            return jsonify({"message": "El correo ya está registrado"}), 400

        # Insertar el nuevo usuario
        values = (data['nombre'], data['apellido'], data['correo'], hashed_password)
        cursor.execute(query_insert, values)
        connection.commit()

        # Redirigir al inicio de sesión
        return redirect('http://127.0.0.1:3609/iniciarSesion')
    except Exception as e:
        return jsonify({'message': f'Error al registrar usuario: {str(e)}'}), 500
    finally:
        if cursor:
            try:
                cursor.close()
            except Exception as e:
                print(f"Error al cerrar el cursor: {e}")
        if connection:
            try:
                connection.close()
            except Exception as e:
                print(f"Error al cerrar la conexión: {e}")

""" BIEN """
@app.route('/usuarios/login', methods=['POST'])
def login_usuario():
    try:
        correo = request.form['correo']
        contrasni = request.form['contrasni']

        query = "SELECT * FROM usuarios WHERE correo = %s"

        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(query, (correo,))
            usuario = cursor.fetchone()

            # Verificar si el usuario existe y la contraseña es correcta
            if usuario and bcrypt.check_password_hash(usuario['contrasni'], contrasni):
                # Guardar datos en la sesión
                session['id_usuarios'] = usuario['id_usuarios']
                session['nombre'] = usuario['nombre']
                print(f"Sesión actual: {dict(session)}")
                return redirect('http://127.0.0.1:3609/index')  # Redirigir al index del frontend
            else:
                return jsonify({"auth": False, "message": "Credenciales incorrectas"}), 401
    except Exception as e:
        print(f"Error en login_usuario: {e}")
        return jsonify({'auth': False, 'message': f'Error al iniciar sesión: {str(e)}'}), 500
    finally:
        connection.close()
""" BIEN """
@app.route('/usuarios/logout', methods=['POST'])
def logout_usuario():
    session.clear()  # Limpiar todas las variables de sesión
    return redirect('http://127.0.0.1:3609/login')

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
# --- Rutas para Kivy ---

@app.route("/api/mascotas-kivy", methods=["GET"])
def mascotas_para_kivy():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT nombre, descripcion, foto, zona, latitud, longitud FROM mascotas")
            mascotas = cursor.fetchall()
        return jsonify(mascotas)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5001)

