CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY, 
    correo VARCHAR(100) NOT NULL UNIQUE,
    contraseña VARCHAR(255)
);


CREATE TABLE mascotas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_usuarios INT,
    nombre VARCHAR(100),
    tipo VARCHAR(100),
    estado VARCHAR(100),
    descripcion TEXT,
    foto BLOB,
    zona VARCHAR(255),
    fecha_publicacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    comentario TEXT,
    FOREIGN KEY (id_usuarios) REFERENCES usuarios(id) ON DELETE CASCADE
);


INSERT INTO usuarios (correo, contraseña) 
VALUES 
('dvidela@gmail.com', 'contraseña123'),
('vgrumelli@gmail.com', 'contraseña456'),
('mprestti@gmail.com', 'contraseña789');

INSERT INTO mascotas (id_usuarios, nombre, tipo, estado, descripcion, zona, comentario)
VALUES 
(1, 'Luna', 'Gato', 'Perdida', 'Gato gris con ojos verdes.', 'Barrio Norte', 'Vi a Luna cerca de la plaza.'),
(2, 'Tomi', 'Perro', 'Perdida', 'Perro labrador de color amarillo.', 'Villa Urquiza', NULL), 
(3, 'Cheems', 'Perro', 'Encontrada', 'Perro encontrado cerca de la estación.', 'Palermo', 'Cheems estaba cerca de plaza Italia.');




