CREATE TABLE usuarios (
    id_usuarios INT AUTO_INCREMENT PRIMARY KEY, 
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    correo VARCHAR(100) NOT NULL UNIQUE,
    contraseña VARCHAR(255),
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
    fecha_comentario DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuarios) REFERENCES usuarios(id_usuarios) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS coordenadas(
    id INT NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(200),
    direccion VARCHAR(200),
    latitud VARCHAR(200) NOT NULL,
    longitud VARCHAR(200) NOT NULL,
    especie VARCHAR(50) NOT NULL,
    PRIMARY KEY (id)
);

INSERT INTO usuarios (nombre, apellido, correo, contraseña) 
VALUES 
('Delfina', 'Videla', 'dvidela@gmail.com', 'contraseña123'),
('Victoria', 'Grumelli', 'vgrumelli@gmail.com', 'contraseña456'),
('Matias', 'Prestti', 'mprestti@gmail.com', 'contraseña789');

INSERT INTO mascotas (id_usuarios, nombre, tipo, estado, descripcion, zona, comentario)
VALUES 
(1, 'Luna', 'Gato', 'Perdida', 'Gato gris con ojos verdes.', 'Barrio Norte', 'Vi a Luna cerca de la plaza.'),
(2, 'Tomi', 'Perro', 'Perdida', 'Perro labrador de color amarillo.', 'Villa Urquiza', NULL), 
(3, 'Cheems', 'Perro', 'Encontrada', 'Perro encontrado cerca de la estación.', 'Palermo', 'Cheems estaba cerca de plaza Italia.'),
(4, 'Copito', 'Conejo', 'Encontrada', 'Conejo blanco con orejas largas.', 'Caballito', 'Visto en el parque Rivadavia.'),
(5, 'Franklin', 'Tortuga', 'Perdida', 'Tortuga pequeña de caparazón oscuro.', 'Villa Crespo', NULL),
(6, 'Mara', 'Perro', 'Perdida', 'Pug tranquila y juguetona.', 'Recoleta', NULL),
(7, 'Bobby', 'Perro', 'Encontrada', 'Golden Retriever amigable.', 'Belgrano', 'Estaba paseando cerca del río.'),
(8, 'Mika', 'Perro', 'Perdida', 'Jack Russell Terrier juguetón.', 'Palermo', 'Visto en el parque Las Heras.');


INSERT INTO coordenadas (nombre,direccion,latitud,longitud,especie)
VALUES ("Ryan","Av. Paseo Colón 250, C1054","-34.610631","-58.369250","gato");
INSERT INTO coordenadas (nombre,direccion,latitud,longitud,especie)
VALUES ("Milo","Av. Rivadavia 717, C1002AAF","-34.608131","-58.376856","gato");
INSERT INTO coordenadas (nombre,direccion,latitud,longitud,especie)
VALUES ("pepito","Jeanette Campbell 4581","-34.675994","-58.455311","perro");
INSERT INTO coordenadas (nombre,direccion,latitud,longitud,especie)
VALUES ("Karen","Av. Rivadavia 6151-6193","-34.625359","-58.453405","gato");
INSERT INTO coordenadas (nombre,direccion,latitud,longitud,especie)
VALUES ("Horacio","Nicaragua 4600-4548, C1414BVF","-34.588418","-58.424974","perro");
INSERT INTO coordenadas (nombre,direccion,latitud,longitud,especie)
VALUES ("Mika","Av. Olazábal 2501-2599, C1428DHH","-34.560870","-58.459699","perro");
INSERT INTO coordenadas (nombre,direccion,latitud,longitud,especie)
VALUES ("Raul","Montañeses 2225, C1428 ","-34.556089","-58.450057","gato");
INSERT INTO coordenadas (nombre,direccion,latitud,longitud,especie)
VALUES ("Huh?","Av. Pres. Figueroa Alcorta 5300-5288, C1426CBP","-34.565176", "-58.420497","gato");
INSERT INTO coordenadas (nombre,direccion,latitud,longitud,especie)
VALUES ("Pancho","Gregorio de Laferrère 2601-2699, C1406HFE","-34.637985", "-58.461345","perro");