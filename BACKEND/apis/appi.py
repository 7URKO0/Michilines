from flask import Flask, jsonify, request, redirect
from flask_bcrypt import Bcrypt
import mysql.connector
import pymysql

app = Flask(__name__)
bcrypt = Bcrypt(app)
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

# --- Rutas para Mascotas ---
@app.route('/mascotas', methods=['GET'])
def obtener_mascotas():
    query = "SELECT * FROM mascotas;"
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(query)
            resultado = cursor.fetchall()
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'message': f'Error al obtener mascotas: {str(e)}'}), 500
    finally:
        connection.close()

@app.route('/mascotas', methods=['POST'])
def agregar_mascota():
    nueva_mascota = request.get_json()
    query = """INSERT INTO mascotas (id_usuarios, nombre, tipo, estado, descripcion, zona, comentario)
               VALUES (%s, %s, %s, %s, %s, %s, %s);"""
    values = (
        nueva_mascota['id_usuarios'], nueva_mascota['nombre'], nueva_mascota['tipo'],
        nueva_mascota['estado'], nueva_mascota['descripcion'], nueva_mascota['zona'],
        nueva_mascota.get('comentario', None)
    )
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(query, values)
            connection.commit()
        return jsonify({'message': 'Mascota agregada exitosamente'}), 201
    except Exception as e:
        return jsonify({'message': f'Error al agregar mascota: {str(e)}'}), 500
    finally:
        connection.close()

@app.route('/mascotas/<int:id>', methods=['PATCH'])
def modificar_mascota(id):
    modificar_mascota = request.get_json()
    campos = ', '.join([f"{key} = %s" for key in modificar_mascota])
    valores = tuple(modificar_mascota.values())
    query = f"UPDATE mascotas SET {campos} WHERE id = %s;"
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(query, valores + (id,))
            connection.commit()
        return jsonify({'message': 'Mascota modificada exitosamente'}), 200
    except Exception as e:
        return jsonify({'message': f'Error al modificar mascota: {str(e)}'}), 500
    finally:
        connection.close()

@app.route('/mascotas/<int:id>', methods=['DELETE'])
def borrar_mascota(id):
    query = "DELETE FROM mascotas WHERE id = %s;"
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(query, (id,))
            connection.commit()
        return jsonify({'message': 'Mascota eliminada exitosamente'}), 200
    except Exception as e:
        return jsonify({'message': f'Error al eliminar mascota: {str(e)}'}), 500
    finally:
        connection.close()

# --- Rutas para Comentarios ---
@app.route('/comentarios', methods=['POST'])
def agregar_comentario():
    nuevo_comentario = request.get_json()
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
        return jsonify({'message': f'Error al agregar comentario: {str(e)}'}), 500
    finally:
        connection.close()

@app.route('/comentarios/<int:id>', methods=['DELETE'])
def borrar_comentario(id):
    query = "DELETE FROM comentarios WHERE id = %s;"
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(query, (id,))
            connection.commit()
        return jsonify({'message': 'Comentario eliminado exitosamente'}), 200
    except Exception as e:
        return jsonify({'message': f'Error al eliminar comentario: {str(e)}'}), 500
    finally:
        connection.close()

# --- Rutas para Usuarios ---
@app.route('/usuarios', methods=['POST'])
def registrar_usuario():
    data = request.form.to_dict()  # Captura datos del formulario en formato clave-valor
    print("Datos recibidos:", data)  # Para depuración

    campos_requeridos = ['nombre', 'apellido', 'correo', 'contrasni', 'confirmarContrasni']
    if not all(campo in data for campo in campos_requeridos):
        return jsonify({"message": "Faltan datos obligatorios"}), 400

    if data['contrasni'] != data['confirmarContrasni']:
        return jsonify({"message": "Las contrasnis no coinciden"}), 400

    hashed_password = bcrypt.generate_password_hash(data['contrasni']).decode('utf-8')
    query = """
        INSERT INTO usuarios (nombre, apellido, correo, contrasni)
        VALUES (%s, %s, %s, %s)
    """
    values = (data['nombre'], data['apellido'], data['correo'], hashed_password)
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE correo = %s", (data['correo'],))
        if cursor.fetchone():
            return jsonify({"message": "El correo ya está registrado"}), 400

        cursor.execute(query, values)
        connection.commit()

        # Redirige al inicio de sesión en el frontend
        return redirect('http://127.0.0.1:3609/iniciarSesion')
    except Exception as e:
        return jsonify({'message': f'Error al registrar usuario: {str(e)}'}), 500
    finally:
        if cursor is not None:
            try:
                cursor.close()
            except Exception as e:
                print(f"Error al cerrar el cursor: {e}")

        if connection is not None:
            try:
                connection.close()
            except Exception as e:
                print(f"Error al cerrar la conexión: {e}")
                

@app.route('/usuarios/login', methods=['POST'])
def login_usuario():
    correo = request.form.get('correo')  # Cambiado para datos de formulario
    contrasni = request.form.get('contrasni')

    if not correo or not contrasni:
        return jsonify({"message": "Correo y contrasni son obligatorios"}), 400

    query = "SELECT * FROM usuarios WHERE correo = %s;"
    try:
        connection = get_db_connection()
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute(query, (correo,))
            usuario = cursor.fetchone()

            # Verificar credenciales
            if usuario and bcrypt.checkpw(contrasni.encode('utf-8'), usuario['contrasni'].encode('utf-8')):
                return jsonify({"message": "Inicio de sesión exitoso", "usuario": usuario}), 200
            else:
                return jsonify({"message": "Credenciales incorrectas"}), 401
    except Exception as e:
        return jsonify({'message': f'Error al iniciar sesión: {str(e)}'}), 500
    finally:
        connection.close()

if __name__ == '__main__':
   app.run("127.0.0.1",debug=True, port=5000)