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

# Verificar si las imágenes existen
imagenes = ["Luna.png", "Tomi.png", "Cheems.png", "Bobby.png", "Copito.png", "Franklin.jpg", "Mara.png"]
for imagen in imagenes:
    ruta = os.path.join(IMAGENES_DIR, imagen)
    if os.path.exists(ruta):
        print(f"{imagen} encontrada en {ruta}")
    else:
        print(f"⚠️ {imagen} no encontrada en {ruta}")

# Función para convertir imágenes a Base64
def convertir_imagen_a_base64(nombre_imagen):
    ruta_imagen = os.path.join(IMAGENES_DIR, nombre_imagen)
    try:
        with open(ruta_imagen, "rb") as archivo:
            return base64.b64encode(archivo.read()).decode("utf-8")
    except FileNotFoundError:
        print(f"⚠️ Imagen no encontrada: {ruta_imagen}")
        return None  # Devuelve `None` si no se encuentra la imagen
    except Exception as e:
        print(f"⚠️ Error al leer la imagen {ruta_imagen}: {e}")
        return None

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
            "foto": "Luna.png",
            "zona": "Barrio Norte",
            "latitud": -34.588621,
            "longitud": -58.411601
        },
        {
            "id_usuarios": 2,
            "nombre": "Tomi",
            "tipo": "Perro",
            "estado": "Perdida",
            "descripcion": "Perro labrador de color amarillo.",
            "foto": "Tomi.png",
            "zona": "Villa Urquiza",
            "latitud": -34.601248,
            "longitud": -58.426735
        },
        {
            "id_usuarios": 3,
            "nombre": "Cheems",
            "tipo": "Perro",
            "estado": "Encontrada",
            "descripcion": "Perro encontrado cerca de la estación.",
            "foto": "Cheems.png",
            "zona": "Palermo",
            "latitud": -34.588107,
            "longitud": -58.430428
        },
        {
            "id_usuarios": 2,
            "nombre": "Bobby",
            "tipo": "Perro",
            "estado": "Encontrado",
            "descripcion": "Perro enérgico y leal",
            "foto": "Bobby.png",
            "zona": "Villa Crespo",
            "latitud": -34.610,
            "longitud": -58.420
        },
        {
            "id_usuarios": 3,
            "nombre": "Copito",
            "tipo": "Conejo",
            "estado": "Encontrado",
            "descripcion": "Conejo amigable y dientón",
            "foto": "Copito.png",
            "zona": "Once",
            "latitud": -34.605,
            "longitud": -58.409
        },
        {
            "id_usuarios": 1,
            "nombre": "Franklin",
            "tipo": "Tortuga",
            "estado": "Perdido",
            "descripcion": "Tortuga tímida e incomprendida",
            "foto": "Franklin.jpg",
            "zona": "Tigre",
            "latitud": -34.426,
            "longitud": -58.579
        },
        {
            "id_usuarios": 2,
            "nombre": "Mara",
            "tipo": "Perra",
            "estado": "Perdido",
            "descripcion": "Perra tranquila",
            "foto": "Mara.png",
            "zona": "Recoleta",
            "latitud": -34.592,
            "longitud": -58.392
        }
    ]

    # Procesar las imágenes a Base64 antes de insertar
    for mascota in mascotas:
        mascota["foto"] = convertir_imagen_a_base64(mascota["foto"])
        if not mascota["foto"]:
            print(f"⚠️ No se pudo procesar la imagen para {mascota['nombre']}. Saltando.")
            continue

    query = """
        INSERT INTO mascotas (id_usuarios, nombre, tipo, estado, descripcion, foto, zona, fecha_publicacion, latitud, longitud)
        VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), %s, %s)
    """

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            for mascota in mascotas:
                if not mascota["foto"]:  # Salta registros sin foto válida
                    continue
                cursor.execute(query, (
                    mascota["id_usuarios"],
                    mascota["nombre"],
                    mascota["tipo"],
                    mascota["estado"],
                    mascota["descripcion"],
                    mascota["foto"],  # Base64 de la imagen
                    mascota["zona"],
                    mascota["latitud"],
                    mascota["longitud"]
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
