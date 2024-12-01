

CREATE table alumnados ( 
	padron INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	nombre VARCHAR(100),
	apellido VARCHAR(100)
)


CREATE table electivas ( 
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	nombre VARCHAR(100),
	comision VARCHAR(100),
	titular INT
)

DROP TABLE test.alumnos, test.electivas , test.electoral , test.materias ;

