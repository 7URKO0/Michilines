from flask import Blueprint, request, jsonify
import pymysql

comentarios_api = Blueprint('comentarios_api', __name__)

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

@comentarios_api.route('/', methods=['GET', 'POST'])
def manejar_comentarios():
    if request.method == 'GET':
        mascota_id = request.args.get('mascota_id')
        if not mascota_id:
            return jsonify({"error": "ID de mascota requerido"}), 400

        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM comentarios WHERE mascota_id = %s", (mascota_id,))
            comentarios = cursor.fetchall()
        conexion.close()
        return jsonify(comentarios), 200

    elif request.method == 'POST':
        data = request.json
        mascota_id = data.get('mascota_id')
        contenido = data.get('contenido')

        if not mascota_id or not contenido:
            return jsonify({"error": "Datos incompletos"}), 400

        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            cursor.execute("""
                INSERT INTO comentarios (contenido, mascota_id)
                VALUES (%s, %s)
            """, (contenido, mascota_id))
        conexion.commit()
        conexion.close()
        return jsonify({"mensaje": "Comentario añadido exitosamente"}), 201
