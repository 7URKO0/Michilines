from flask import Flask, jsonify, request, redirect, session
from flask_bcrypt import Bcrypt  # Solo Flask-Bcrypt
import pymysql.cursors
import base64
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
@app.route('/mascotas', methods=['POST'])
def agregar_mascota():
    if 'id_usuarios' not in session:
        return jsonify({"auth": False, "message": "Usuario no autenticado"}), 401

    try:
        id_usuarios = session['id_usuarios']
        nombre = request.form.get('nombre')
        tipo = request.form.get('tipo')
        estado = request.form.get('estado')
        descripcion = request.form.get('descripcion')
        zona = request.form.get('zona', 'No especificada')

        # Verificar archivo recibido
        foto = request.files.get('foto')
        if foto:
            print(f"Archivo recibido: {foto.filename}")
            foto_bytes = foto.read()
            print(f"Tamaño del archivo recibido: {len(foto_bytes)} bytes")
            foto_base64 = base64.b64encode(foto_bytes).decode('utf-8')
        else:
            print("No se recibió archivo de foto")
            foto_base64 = None

        if not all([nombre, tipo, estado, descripcion]):
            return jsonify({"message": "Faltan datos obligatorios"}), 400

        # Guardar en base de datos
        query = """
            INSERT INTO mascotas (id_usuarios, nombre, tipo, estado, descripcion, foto, zona, fecha_publicacion)
            VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
        """
        valores = (id_usuarios, nombre, tipo, estado, descripcion, foto_base64, zona)
        
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(query, valores)
            connection.commit()

        return jsonify({"message": "Mascota publicada exitosamente"}), 201
    except Exception as e:
        print(f"Error en agregar_mascota: {str(e)}")
        return jsonify({"message": "Error al procesar la solicitud"}), 500



@app.route('/mascotas/<int:id>', methods=['DELETE'])
def eliminar_mascota(id):
    if 'id_usuarios' not in session:
        print("Usuario no autenticado.")
        return jsonify({"auth": False, "message": "Usuario no autenticado"}), 401

    query = "DELETE FROM mascotas WHERE id = %s"
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(query, (id,))
            connection.commit()
            if cursor.rowcount == 0:
                print(f"Mascota con ID {id} no encontrada.")
                return jsonify({"message": "Mascota no encontrada"}), 404
            print(f"Mascota con ID {id} eliminada exitosamente.")
        return jsonify({"message": "Mascota eliminada exitosamente"}), 200
    except Exception as e:
        print(f"Error en eliminar_mascota: {e}")
        return jsonify({'message': f'Error al eliminar mascota: {str(e)}'}), 500
    finally:
        connection.close()




@app.route('/mascotas', methods=['GET'])
def obtener_mascotas():
    query = "SELECT id, nombre, tipo, estado, descripcion, zona, foto FROM mascotas;"
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(query)
            resultado = cursor.fetchall()

            for mascota in resultado:
                if mascota.get('foto'):
                    mascota['foto'] = base64.b64encode(mascota['foto']).decode('utf-8')
                else:
                    mascota['foto'] = None  # Si no hay imagen, deja `None`

            return jsonify(resultado), 200
    except Exception as e:
        print(f"Error en obtener_mascotas: {e}")
        return jsonify({'message': f'Error al obtener mascotas: {str(e)}'}), 500
    finally:
        connection.close()

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
# --- Rutas para Comentarios ---
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


@app.route('/mascotas/<int:id>', methods=['GET'])
def obtener_perfil_mascota(id):
    query = "SELECT id, nombre, tipo, estado, descripcion, zona, foto FROM mascotas WHERE id = %s;"
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(query, (id,))
            resultado = cursor.fetchone()

            if resultado:
                if resultado.get('foto'):
                    resultado['foto'] = base64.b64encode(resultado['foto']).decode('utf-8')
                return jsonify(resultado), 200
            else:
                return jsonify({'message': 'Mascota no encontrada'}), 404
    except Exception as e:
        print(f"Error en obtener_perfil_mascota: {e}")
        return jsonify({'message': f'Error al obtener perfil de la mascota: {str(e)}'}), 500
    finally:
        connection.close()
        
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
# --- Rutas para Usuarios ---
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
    
@app.route('/usuarios/logout', methods=['POST'])
def logout_usuario():
    session.clear()  # Limpiar todas las variables de sesión
    return redirect('http://127.0.0.1:3609/login')


@app.route('/mascotas/<int:id>/foto', methods=['GET'])
def obtener_foto(id):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            query = "SELECT foto FROM mascotas WHERE id = %s"
            cursor.execute(query, (id,))
            resultado = cursor.fetchone()
            if resultado and resultado['foto']:
                with open(f"foto_{id}.jpg", "wb") as f:
                    f.write(resultado['foto'])
                return send_file(f"foto_{id}.jpg", mimetype='image/jpeg')
            else:
                return jsonify({"message": "Foto no encontrada"}), 404
    except Exception as e:
        return jsonify({"message": f"Error al obtener foto: {str(e)}"}), 500


if __name__ == '__main__':
   app.run("127.0.0.1",debug=True, port=5000)