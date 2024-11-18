from flask import Blueprint, request, jsonify
import pymysql
import hashlib

usuarios_api = Blueprint('usuarios_api', __name__)

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

def hash_password(password):
    """Genera un hash seguro para la contraseña."""
    return hashlib.sha256(password.encode()).hexdigest()

@usuarios_api.route('/registrarse', methods=['POST'])
def registrarse():
    """Registra a un nuevo usuario."""
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Faltan datos"}), 400

    hashed_password = hash_password(password)

    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id FROM usuarios WHERE username = %s", (username,))
        if cursor.fetchone():
            return jsonify({"error": "El usuario ya existe"}), 409
        cursor.execute("INSERT INTO usuarios (username, password) VALUES (%s, %s)", (username, hashed_password))
    conexion.commit()
    conexion.close()

    return jsonify({"mensaje": "Usuario registrado exitosamente"}), 201

@usuarios_api.route('/login', methods=['POST'])
def login():
    """Autentica a un usuario."""
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Faltan datos"}), 400

    hashed_password = hash_password(password)

    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT id FROM usuarios WHERE username = %s AND password = %s", (username, hashed_password))
        usuario = cursor.fetchone()

    conexion.close()

    if usuario:
        return jsonify({"mensaje": "Inicio de sesión exitoso", "usuario_id": usuario['id']}), 200
    return jsonify({"error": "Credenciales incorrectas"}), 401
