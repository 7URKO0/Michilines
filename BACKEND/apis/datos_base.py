import os
import base64
import pymysql.cursors

# Configuración de la base de datos
def get_db_connection():
    db_config = {
        "host": "localhost",
        "port": 3307,
        "user": "powpatrol",
        "password": "Powpatrol1.",
        "database": "pawbase",
        "cursorclass": pymysql.cursors.DictCursor
    }
    return pymysql.connect(**db_config)

# Calcular la ruta absoluta del directorio del proyecto
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))  # Subir dos niveles
IMAGENES_DIR = os.path.join(BASE_DIR, "FRONTEND", "static", "imagenes")  # Ruta a las imágenes

# Función para convertir imágenes a Base64
def convertir_imagen_a_base64(nombre_imagen):
    ruta_imagen = os.path.join(IMAGENES_DIR, nombre_imagen)
    if not os.path.exists(ruta_imagen):
        raise FileNotFoundError(f"No se encontró la imagen: {ruta_imagen}")
    with open(ruta_imagen, "rb") as archivo:
        return base64.b64encode(archivo.read()).decode("utf-8")

# Función para insertar datos en la tabla mascotas
def insertar_mascotas():
    # Datos iniciales
    mascotas = [
        {
            "id_usuarios": 1,
            "nombre": "Luna",
            "tipo": "Gato",
            "estado": "Perdida",
            "descripcion": "Gato gris con ojos verdes.",
            "foto": convertir_imagen_a_base64("Luna.png"),
            "zona": "Barrio Norte"
        },
        {
            "id_usuarios": 2,
            "nombre": "Tomi",
            "tipo": "Perro",
            "estado": "Perdida",
            "descripcion": "Perro labrador de color amarillo.",
            "foto": convertir_imagen_a_base64("Tomi.png"),
            "zona": "Villa Urquiza"
        },
        {
            "id_usuarios": 3,
            "nombre": "Cheems",
            "tipo": "Perro",
            "estado": "Encontrada",
            "descripcion": "Perro encontrado cerca de la estación.",
            "foto": convertir_imagen_a_base64("Cheems.png"),
            "zona": "Palermo"
        }
    ]

    query = """
        INSERT INTO mascotas (id_usuarios, nombre, tipo, estado, descripcion, foto, zona, fecha_publicacion)
        VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
    """

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            for mascota in mascotas:
                cursor.execute(query, (
                    mascota["id_usuarios"],
                    mascota["nombre"],
                    mascota["tipo"],
                    mascota["estado"],
                    mascota["descripcion"],
                    mascota["foto"],  # Base64 de la imagen
                    mascota["zona"]
                ))
            connection.commit()
            print("¡Datos de mascotas insertados correctamente!")
    except Exception as e:
        print(f"Error al insertar datos: {e}")
    finally:
        connection.close()

# Ejecutar el script
if __name__ == "__main__":
    insertar_mascotas()
