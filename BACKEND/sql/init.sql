-- Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS pawbase;
USE pawbase;

-- Crear la tabla usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuarios INT AUTO_INCREMENT PRIMARY KEY, 
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    correo VARCHAR(100) NOT NULL UNIQUE,
    contrasni VARCHAR(255) NOT NULL,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear la tabla mascotas
CREATE TABLE IF NOT EXISTS mascotas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_usuarios INT NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    tipo VARCHAR(100) NOT NULL,
    estado VARCHAR(100) NOT NULL,
    descripcion TEXT,
    foto LONGTEXT,
    zona VARCHAR(255),
    fecha_publicacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuarios) REFERENCES usuarios(id_usuarios) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS comentarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_mascota INT NOT NULL,
    id_usuario INT NOT NULL,
    texto TEXT NOT NULL,
    fecha_comentario DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_mascota) REFERENCES mascotas(id) ON DELETE CASCADE,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuarios) ON DELETE CASCADE
);


-- Crear la tabla coordenadas
CREATE TABLE IF NOT EXISTS coordenadas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    direccion VARCHAR(200) NOT NULL,
    latitud DECIMAL(10, 8) NOT NULL,
    longitud DECIMAL(11, 8) NOT NULL,
    especie VARCHAR(50) NOT NULL
);

-- Insertar datos en la tabla usuarios
INSERT INTO usuarios (nombre, apellido, correo, contrasni) 
VALUES 
('Delfina', 'Videla', 'dvidela@gmail.com', '$2b$12$K9z/XKXI2m1T1z5E5jfG1ujRGf4f9X4mkDAWzWQdfg3XEF4Lh/aPi'),
('Victoria', 'Grumelli', 'vgrumelli@gmail.com', '$2b$12$LPa4thKImf7RtykmKNu2/uXMzd/r4PGzZIFXuf7kk9Wes4MaY7JCa'),
('Matias', 'Prestti', 'mprestti@gmail.com', '$2b$12$y1EsA9XFYP1FWkfq6tGczOxCQeJZqM9h91ED0grGyJcMHFB8YNkaG');

/* -- Insertar datos en la tabla mascotas
INSERT INTO mascotas (id_usuarios, nombre, tipo, estado, descripcion, zona, comentario)
VALUES 
(1, 'Luna', 'Gato', 'Perdida', 'Gato gris con ojos verdes.', 'Barrio Norte', 'Vi a Luna cerca de la plaza.'),
(2, 'Tomi', 'Perro', 'Perdida', 'Perro labrador de color amarillo.', 'Villa Urquiza', NULL), 
(3, 'Cheems', 'Perro', 'Encontrada', 'Perro encontrado cerca de la estación.', 'Palermo', 'Cheems estaba cerca de plaza Italia.'); */

-- Insertar datos en la tabla coordenadas
INSERT INTO coordenadas (nombre, direccion, latitud, longitud, especie)
VALUES 
('domi', 'Av. Paseo Colón 250, C1054', -34.610631, -58.369250, 'gato'),
('fer', 'Av. Rivadavia 717, C1002AAF', -34.608131, -58.376856, 'gato'),
('yai', 'Jeanette Campbell 4581', -34.675994, -58.455311, 'perro');
