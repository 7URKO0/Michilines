from flask import Flask, request, jsonify
import pymysql
import hashlib

app = Flask(__name__)

connection = mysql.connector.connect(
    host='db',              
    user='powpatrol',        
    password='Powpatrol1.',  
    database='pawbase',      
    port='3306'              
)
cursor = connection.cursor()


@app.route('/mascotas', methods=['GET'])
def obtener_mascotas():
    query = "SELECT id, id_usuarios, nombre, tipo, estado, descripcion, zona, fecha_publicacion FROM mascotas;"
    try:
        cursor.execute(query)
        resultado = cursor.fetchall()
    except SQLAlchemyError as err:
       return jsonify({'message': 'Error: ' + str(err)}), 500
    
    data = []
    for row in resultado:
        diccionario = {
            'id': row[0],
            'id_usuarios': row[1],
            'nombre': row[2],
            'tipo': row[3],
            'estado': row[4],
            'descripcion': row[5],
            'zona': row[6],
            'fecha_publicacion': row[7]
        }
        data.append(diccionario)
    return jsonify(data), 200

@app.route('/mascotas', methods=['GET'])
def obtener_mascotas():
    query = "SELECT * FROM mascotas;"
    try:
        cursor.execute(query)
        resultado = cursor.fetchall()
        data = [{'id': row[0], 'id_usuarios': row[1], 'nombre': row[2], 'tipo': row[3], 'estado': row[4], 
                 'descripcion': row[5], 'zona': row[6], 'fecha_publicacion': row[7]} for row in resultado]
    except Exception as e:
        return jsonify({'message': f'Error al obtener mascotas: {str(e)}'}), 500
    return jsonify(data), 200

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
        cursor.execute(query, values)
        connection.commit()
    except Exception as e:
        return jsonify({'message': f'Error al agregar mascota: {str(e)}'}), 500
    return jsonify({'message': 'Mascota agregada exitosamente'}), 201

@app.route('/mascotas/<int:id>', methods=['PATCH'])
def modificar_mascota(id):
    modificar_mascota = request.get_json()
    campos = ', '.join([f"{key} = %s" for key in modificar_mascota])
    valores = tuple(modificar_mascota.values())
    query = f"UPDATE mascotas SET {campos} WHERE id = %s;"
    try:
        cursor.execute(query, valores + (id,))
        connection.commit()
    except Exception as e:
        return jsonify({'message': f'Error al modificar mascota: {str(e)}'}), 500
    return jsonify({'message': 'Mascota modificada exitosamente'}), 200

@app.route('/mascotas/<int:id>', methods=['DELETE'])
def borrar_mascota(id):
    query = "DELETE FROM mascotas WHERE id = %s;"
    try:
        cursor.execute(query, (id,))
        connection.commit()
    except Exception as e:
        return jsonify({'message': f'Error al eliminar mascota: {str(e)}'}), 500
    return jsonify({'message': 'Mascota eliminada exitosamente'}), 200

@usuarios_api.route('/api/usuarios', methods=['POST'])
def registrar_usuario():
    data = request.json

    # Validar datos requeridos
    campos_requeridos = ['nombre', 'apellido', 'correo', 'contraseña']
    if not all(campo in data for campo in campos_requeridos):
        return jsonify({"message": "Faltan datos obligatorios"}), 400

    # Conexión a la base de datos
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        # Verificar si el correo ya está registrado
        cursor.execute("SELECT * FROM usuarios WHERE correo = %s", (data['correo'],))
        if cursor.fetchone():
            return jsonify({"message": "El correo ya está registrado"}), 400

        # Registrar el nuevo usuario
        cursor.execute("""
            INSERT INTO usuarios (nombre, apellido, correo, contraseña)
            VALUES (%s, %s, %s, %s)
        """, (data['nombre'], data['apellido'], data['correo'], data['contraseña']))
    conexion.commit()
    conexion.close()

    return jsonify({"message": "Usuario registrado exitosamente"}), 201

if __name__ == '__main__':
    app.run(debug=True)

