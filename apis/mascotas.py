from flask import Blueprint, request, jsonify
import pymysql

mascotas_api = Blueprint('mascotas_api', __name__)

DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'michilines_usuario'
DB_NAME = 'michilines'

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
    if request.method == 'GET':
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

    elif request.method == 'POST':
        data = request.json
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

    elif request.method == 'PUT':
        data = request.json
        mascota_id = data.get('id')
        if not mascota_id:
            return jsonify({"error": "ID de mascota requerido"}), 400

        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("""
                UPDATE mascotas
                SET nombre = %s, descripcion = %s, imagen_url = %s, edad = %s, raza = %s, zona = %s, estado = %s
                WHERE id = %s
            """, (
                data['nombre'], 
                data['descripcion'], 
                data['imagen_url'], 
                data['edad'], 
                data['raza'], 
                data['zona'], 
                data['estado'], 
                mascota_id
            ))
        conexion.commit()
        conexion.close()
        return jsonify({"mensaje": "Mascota actualizada exitosamente"}), 200

    elif request.method == 'DELETE':
        mascota_id = request.args.get('id')
        if not mascota_id:
            return jsonify({"error": "ID de mascota requerido"}), 400

        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("DELETE FROM mascotas WHERE id = %s", (mascota_id,))
        conexion.commit()
        conexion.close()
        return jsonify({"mensaje": "Mascota eliminada exitosamente"}), 200
