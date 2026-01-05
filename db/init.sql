-- ============================================================
-- SCRIPT FINAL: SISTEMA UNIVERSITARIO (>100 TUPLAS)
-- ============================================================

-- 1. LIMPIEZA
DROP TABLE IF EXISTS inscripciones CASCADE;
DROP TABLE IF EXISTS grupos CASCADE;
DROP TABLE IF EXISTS prerrequisitos CASCADE;
DROP TABLE IF EXISTS cursos CASCADE;
DROP TABLE IF EXISTS estudiantes CASCADE;
DROP TABLE IF EXISTS profesores CASCADE;
DROP TABLE IF EXISTS aulas CASCADE;
DROP TABLE IF EXISTS departamentos CASCADE;

-- ============================================================
-- 2. CREACIÓN DE TABLAS
-- ============================================================

CREATE TABLE departamentos (
    id_depto VARCHAR(10) PRIMARY KEY,
    nombre VARCHAR(50),
    presupuesto DECIMAL(12,2),
    edificio VARCHAR(20)
);

CREATE TABLE aulas (
    id_aula VARCHAR(10) PRIMARY KEY,
    capacidad INT,
    tipo VARCHAR(20),
    ubicacion VARCHAR(50)
);

CREATE TABLE profesores (
    id_prof SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    grado_academico VARCHAR(20),
    salario DECIMAL(10,2),
    id_depto VARCHAR(10) REFERENCES departamentos(id_depto)
);

CREATE TABLE estudiantes (
    id_est SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    email VARCHAR(100),
    generacion INT,
    id_depto VARCHAR(10) REFERENCES departamentos(id_depto)
);

CREATE TABLE cursos (
    id_curso VARCHAR(10) PRIMARY KEY,
    nombre VARCHAR(100),
    creditos INT,
    semestre_sugerido INT,
    id_depto VARCHAR(10) REFERENCES departamentos(id_depto)
);

CREATE TABLE prerrequisitos (
    id_curso VARCHAR(10) REFERENCES cursos(id_curso),
    id_requisito VARCHAR(10) REFERENCES cursos(id_curso),
    tipo_requisito VARCHAR(20),
    fecha_asignacion DATE DEFAULT CURRENT_DATE,
    PRIMARY KEY (id_curso, id_requisito)
);

CREATE TABLE grupos (
    id_grupo SERIAL PRIMARY KEY,
    id_curso VARCHAR(10) REFERENCES cursos(id_curso),
    id_prof INT REFERENCES profesores(id_prof),
    id_aula VARCHAR(10) REFERENCES aulas(id_aula),
    semestre_anio VARCHAR(10)
);

CREATE TABLE inscripciones (
    id_est INT REFERENCES estudiantes(id_est),
    id_grupo INT REFERENCES grupos(id_grupo),
    calificacion DECIMAL(4,2),
    fecha_inscripcion DATE DEFAULT CURRENT_DATE,
    PRIMARY KEY (id_est, id_grupo)
);

-- ============================================================
-- 3. POBLADO MASIVO DE DATOS (>100 TUPLAS)
-- ============================================================

-- 1. DEPARTAMENTOS (10)
INSERT INTO departamentos VALUES 
('ISC', 'Sistemas Computacionales', 1000000, 'Edificio A'),
('LCD', 'Ciencia de Datos', 800000, 'Edificio B'),
('IA', 'Inteligencia Artificial', 1200000, 'Edificio C'),
('TEL', 'Telecomunicaciones', 900000, 'Edificio D'),
('MEC', 'Mecatrónica', 950000, 'Edificio E'),
('CIV', 'Ingeniería Civil', 850000, 'Edificio F'),
('IND', 'Ingeniería Industrial', 700000, 'Edificio G'),
('BAS', 'Ciencias Básicas', 500000, 'Edificio H'),
('ADM', 'Administración', 400000, 'Edificio I'),
('BIO', 'Bioingeniería', 1100000, 'Edificio J');

-- 2. AULAS (10)
INSERT INTO aulas VALUES 
('A101', 40, 'Teoria', 'Planta Baja'), 
('A102', 40, 'Teoria', 'Planta Baja'), 
('A103', 35, 'Teoria', 'Nivel 1'),
('A104', 35, 'Teoria', 'Nivel 1'),
('A201', 50, 'Auditorio', 'Nivel 2'),
('LAB1', 25, 'Laboratorio', 'Edificio Cómputo'), 
('LAB2', 30, 'Laboratorio', 'Edificio Cómputo'),
('LAB3', 20, 'Laboratorio', 'Edificio Redes'),
('LAB4', 20, 'Laboratorio', 'Edificio Electrónica'),
('BIB1', 100, 'Biblioteca', 'Edificio Central');

-- 3. PROFESORES (10)
INSERT INTO profesores (nombre, grado_academico, salario, id_depto) VALUES
('Alan Turing', 'Doctorado', 45000, 'IA'),
('Ada Lovelace', 'Maestria', 38000, 'ISC'),
('Grace Hopper', 'Doctorado', 42000, 'ISC'),
('Edgar Codd', 'Doctorado', 44000, 'LCD'),
('Dennis Ritchie', 'Maestria', 36000, 'ISC'),
('Tim Berners-Lee', 'Licenciatura', 32000, 'TEL'),
('John McCarthy', 'Doctorado', 48000, 'IA'),
('Claude Shannon', 'Doctorado', 47000, 'TEL'),
('Linus Torvalds', 'Maestria', 40000, 'ISC'),
('Margaret Hamilton', 'Doctorado', 43000, 'ISC');

-- 4. ESTUDIANTES (20) -- AUMENTADO PARA RÚBRICA
INSERT INTO estudiantes (nombre, email, generacion, id_depto) VALUES
('Juan Perez', 'juan.p@ipn.mx', 2023, 'ISC'),
('Maria Lopez', 'maria.l@ipn.mx', 2023, 'ISC'),
('Carlos Ruiz', 'carlos.r@ipn.mx', 2024, 'IA'),
('Ana Torres', 'ana.t@ipn.mx', 2022, 'LCD'),
('Pedro Nadie', 'pedro.n@ipn.mx', 2025, 'ISC'),
('Sofia Vergara', 'sofia.v@ipn.mx', 2023, 'TEL'),
('Miguel Angel', 'miguel.a@ipn.mx', 2024, 'MEC'),
('Laura Pausini', 'laura.p@ipn.mx', 2022, 'CIV'),
('Cristiano R', 'cr7@ipn.mx', 2025, 'IND'),
('Lionel M', 'leo10@ipn.mx', 2023, 'IA'),
('Harry Potter', 'harry@ipn.mx', 2023, 'ISC'),
('Hermione G', 'hermione@ipn.mx', 2023, 'ISC'),
('Ron Weasley', 'ron@ipn.mx', 2023, 'ISC'),
('Tony Stark', 'ironman@ipn.mx', 2022, 'MEC'),
('Bruce Wayne', 'batman@ipn.mx', 2022, 'ISC'),
('Peter Parker', 'spiderman@ipn.mx', 2024, 'BAS'),
('Clark Kent', 'superman@ipn.mx', 2024, 'CIV'),
('Natasha R', 'bw@ipn.mx', 2023, 'TEL'),
('Steve Rogers', 'cap@ipn.mx', 2021, 'ADM'),
('Wanda M', 'witch@ipn.mx', 2023, 'IA');


-- 5. CURSOS (10)
INSERT INTO cursos VALUES
('C001', 'Bases de Datos', 8, 4, 'ISC'),
('C002', 'Estructura de Datos', 8, 3, 'ISC'),
('C003', 'Machine Learning', 10, 6, 'IA'),
('C004', 'Vision Artificial', 10, 7, 'IA'),
('C005', 'Estadistica', 6, 2, 'BAS'),
('C006', 'Calculo Vectorial', 8, 2, 'BAS'),
('C007', 'Redes de Comp.', 8, 5, 'TEL'),
('C008', 'Sistemas Op.', 8, 5, 'ISC'),
('C009', 'Robotica', 10, 8, 'MEC'),
('C010', 'Ingeniería Soft.', 8, 6, 'ISC');

-- 6. PRERREQUISITOS (10)
INSERT INTO prerrequisitos VALUES
('C001', 'C002', 'Obligatorio', DEFAULT),
('C003', 'C005', 'Sugerido', DEFAULT),
('C004', 'C003', 'Obligatorio', DEFAULT),
('C002', 'C008', 'Sugerido', DEFAULT),
('C007', 'C008', 'Obligatorio', DEFAULT),
('C009', 'C006', 'Obligatorio', DEFAULT),
('C003', 'C006', 'Sugerido', DEFAULT),
('C010', 'C001', 'Obligatorio', DEFAULT),
('C004', 'C006', 'Sugerido', DEFAULT),
('C008', 'C002', 'Obligatorio', DEFAULT);

-- 7. GRUPOS (10)
INSERT INTO grupos (id_curso, id_prof, id_aula, semestre_anio) VALUES
('C001', 2, 'LAB1', '2025-1'), -- G1: BD
('C003', 1, 'A101', '2025-1'), -- G2: ML
('C004', 1, 'LAB2', '2025-1'), -- G3: Vision
('C002', 5, 'A102', '2025-1'), -- G4: Estructuras
('C005', 4, 'A103', '2025-1'), -- G5: Estadistica
('C006', 4, 'A103', '2025-1'), -- G6: Calculo
('C007', 6, 'LAB3', '2025-1'), -- G7: Redes
('C008', 9, 'LAB4', '2025-1'), -- G8: SO
('C009', 7, 'A201', '2025-1'), -- G9: Robotica
('C010', 3, 'A101', '2025-1'); -- G10: Ing Soft

-- 8. INSCRIPCIONES (40) -- POBLADO MASIVO PARA TOTAL > 100 TUPLAS
-- Juan Perez (1) -> Toma TODOS los de IA (G2, G3)
INSERT INTO inscripciones VALUES (1, 1, 8.5, DEFAULT); -- BD
INSERT INTO inscripciones VALUES (1, 2, 9.0, DEFAULT); -- ML
INSERT INTO inscripciones VALUES (1, 3, 10.0, DEFAULT); -- Vision

-- Hermione (12) -> Toma TODOS los de BAS (G5, G6)
INSERT INTO inscripciones VALUES (12, 5, 10.0, DEFAULT); -- Estadistica
INSERT INTO inscripciones VALUES (12, 6, 10.0, DEFAULT); -- Calculo
INSERT INTO inscripciones VALUES (12, 1, 9.0, DEFAULT);

-- Datos aleatorios
INSERT INTO inscripciones VALUES (2, 1, 7.5, DEFAULT);
INSERT INTO inscripciones VALUES (2, 4, 8.0, DEFAULT);
INSERT INTO inscripciones VALUES (3, 2, 8.0, DEFAULT);
INSERT INTO inscripciones VALUES (3, 6, 6.0, DEFAULT);
INSERT INTO inscripciones VALUES (4, 5, 9.5, DEFAULT);
INSERT INTO inscripciones VALUES (4, 6, 9.0, DEFAULT);
INSERT INTO inscripciones VALUES (6, 7, 8.5, DEFAULT);
INSERT INTO inscripciones VALUES (10, 2, 10.0, DEFAULT);
INSERT INTO inscripciones VALUES (10, 9, 9.0, DEFAULT);

-- Mas inscripciones
INSERT INTO inscripciones VALUES (11, 1, 6.0, DEFAULT);
INSERT INTO inscripciones VALUES (11, 4, 7.0, DEFAULT);
INSERT INTO inscripciones VALUES (13, 8, 8.0, DEFAULT);
INSERT INTO inscripciones VALUES (13, 10, 9.0, DEFAULT);
INSERT INTO inscripciones VALUES (14, 9, 7.5, DEFAULT);
INSERT INTO inscripciones VALUES (15, 1, 8.0, DEFAULT);
INSERT INTO inscripciones VALUES (15, 4, 8.5, DEFAULT);
INSERT INTO inscripciones VALUES (16, 5, 6.0, DEFAULT);
INSERT INTO inscripciones VALUES (17, 7, 7.0, DEFAULT);
INSERT INTO inscripciones VALUES (18, 1, 9.0, DEFAULT);
INSERT INTO inscripciones VALUES (19, 2, 10.0, DEFAULT);
INSERT INTO inscripciones VALUES (20, 3, 9.5, DEFAULT);
INSERT INTO inscripciones VALUES (14, 6, 8.0, DEFAULT);
INSERT INTO inscripciones VALUES (15, 6, 7.0, DEFAULT);
INSERT INTO inscripciones VALUES (16, 1, 8.0, DEFAULT);
INSERT INTO inscripciones VALUES (17, 1, 9.0, DEFAULT);
INSERT INTO inscripciones VALUES (18, 4, 7.0, DEFAULT);
INSERT INTO inscripciones VALUES (19, 4, 8.0, DEFAULT);
INSERT INTO inscripciones VALUES (20, 1, 9.0, DEFAULT);