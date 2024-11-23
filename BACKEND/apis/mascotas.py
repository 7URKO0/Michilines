from flask import Blueprint, request, jsonify
import pymysql

mascotas_api = Blueprint('mascotas_api', __name__)

DB_HOST = 'localhost'
DB_USER = 'powpatrol'
DB_PASSWORD = 'Powpatrol1.'
DB_NAME = 'pawbase'

def obtener_conexion():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )


@mascotas_api.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def manejar_mascotas():
    try:
        if request.method == 'GET':
            return obtener_mascotas()
        elif request.method == 'POST':
            return crear_mascota()
        elif request.method == 'PUT':
            return actualizar_mascota()
        elif request.method == 'DELETE':
            return eliminar_mascota()
    except Exception as e:
        return jsonify({"error": f"Se produjo un error: {str(e)}"}), 500

def obtener_mascotas():
    """Obtiene una o todas las mascotas."""
    mascota_id = request.args.get('id')
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        if mascota_id:
            cursor.execute("SELECT * FROM mascotas WHERE id = %s", (mascota_id,))
            mascota = cursor.fetchone()
            conexion.close()
            if mascota:
                return jsonify(mascota), 200
            return jsonify({"error": "Mascota no encontrada"}), 404
        else:
            cursor.execute("SELECT * FROM mascotas")
            mascotas = cursor.fetchall()
            conexion.close()
            return jsonify(mascotas), 200

def crear_mascota():
    """Crea una nueva mascota."""
    data = request.json
    campos_requeridos = ['nombre', 'descripcion', 'imagen_url', 'edad', 'raza', 'zona', 'estado']
    if not all(campo in data for campo in campos_requeridos):
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("""
            INSERT INTO mascotas (nombre, descripcion, imagen_url, edad, raza, zona, estado)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            data['nombre'], 
            data['descripcion'], 
            data['imagen_url'], 
            data['edad'], 
            data['raza'], 
            data['zona'], 
            data['estado']
        ))
    conexion.commit()
    conexion.close()
    return jsonify({"mensaje": "Mascota creada exitosamente"}), 201

def actualizar_mascota():
    """Actualiza una mascota existente."""
    data = request.json
    mascota_id = data.get('id')
    if not mascota_id:
        return jsonify({"error": "ID de mascota requerido"}), 400

    campos_actualizables = ['nombre', 'descripcion', 'imagen_url', 'edad', 'raza', 'zona', 'estado']
    actualizaciones = {key: data[key] for key in campos_actualizables if key in data}

    if not actualizaciones:
        return jsonify({"error": "No hay campos para actualizar"}), 400

    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        set_clause = ", ".join([f"{key} = %s" for key in actualizaciones.keys()])
        query = f"UPDATE mascotas SET {set_clause} WHERE id = %s"
        cursor.execute(query, list(actualizaciones.values()) + [mascota_id])
    conexion.commit()
    conexion.close()
    return jsonify({"mensaje": "Mascota actualizada exitosamente"}), 200

def eliminar_mascota():
    """Elimina una mascota por ID."""
    mascota_id = request.args.get('id')
    if not mascota_id:
        return jsonify({"error": "ID de mascota requerido"}), 400

    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM mascotas WHERE id = %s", (mascota_id,))
    conexion.commit()
    conexion.close()
    return jsonify({"mensaje": "Mascota eliminada exitosamente"}), 200