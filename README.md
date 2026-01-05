Sistema Universitario – Gestión Académica con Álgebra Relacional y SQL 🎓

Este proyecto implementa un **sistema de base de datos para un entorno universitario**, demostrando la **equivalencia y aplicación práctica del Álgebra Relacional, el Cálculo Relacional y SQL estándar**.

El sistema está **completamente dockerizado** e incluye un **menú interactivo en Python** que permite ejecutar y visualizar **20 consultas complejas**, cumpliendo con la **Modalidad B (Solo Repositorio)** de la práctica.

---

## 👥 Integrantes del Equipo

* Estrada González Naomi Judith

* Herrera Zaragoza Elizabeth

* Romero Martínez Diego Enrique

Grupo: **3CV2**
Materia: **Bases de Datos**
Profesor: **Hurtado Avilés Gabriel**

---

## 📋 Descripción del Dominio

El proyecto modela un **Sistema Universitario**, permitiendo la gestión y análisis de información académica realista, incluyendo:

* **Estudiantes:** Datos personales y de control escolar.
* **Profesores:** Información académica y adscripción a departamentos.
* **Cursos:** Materias impartidas con créditos y prerrequisitos.
* **Grupos:** Asignación de cursos a profesores y aulas.
* **Inscripciones:** Relación entre estudiantes y grupos, con calificaciones.
* **Departamentos:** Organización académica de profesores y cursos.
* **Aulas:** Espacios físicos asignados a los grupos.

Este dominio es ideal para formular consultas complejas con operadores relacionales, cuantificadores lógicos y agregaciones.

---

## 🧩 Modelo Relacional (Esquema)

DEPARTAMENTOS (id_departamento PK, nombre, edificio)

PROFESORES (id_profesor PK, nombre, edad, especialidad, id_departamento FK)

ESTUDIANTES (id_estudiante PK, nombre, edad, carrera, semestre)

CURSOS (id_curso PK, nombre, creditos, id_departamento FK)

PRERREQUISITOS (id_curso FK, id_prerrequisito FK)

AULAS (id_aula PK, edificio, capacidad)

GRUPOS (id_grupo PK, id_curso FK, id_profesor FK, id_aula FK, horario)

INSCRIPCIONES (id_estudiante FK, id_grupo FK, calificacion, fecha_inscripcion)

📌 El archivo `db/init.sql` contiene la creación del esquema y **más de 100 tuplas de datos de ejemplo**.

---

## 📊 Diagrama del Esquema (EER)

El Diagrama Entidad–Relación Extendido representa las entidades del sistema, sus relaciones y cardinalidades, sirviendo como base para el modelo relacional implementado.

---

## 📂 Estructura del Repositorio

```
practica-bd-algebra/
├── docker-compose.yml      # Orquestador de servicios (App + DB)
├── README.md               # Documentación principal
├── app/
│   ├── Dockerfile          # Imagen de la aplicación Python
│   ├── main.py             # Menú interactivo de consultas
│   └── requirements.txt    # Dependencias (psycopg2, tabulate)
└── db/
    └── init.sql            # Esquema y datos de la base de datos
```

---

## 🚀 Instalación y Ejecución

Este proyecto utiliza **Docker y Docker Compose**, por lo que **no es necesario instalar PostgreSQL ni Python localmente**.

### Prerrequisitos

* Docker Desktop (o Docker Engine + Docker Compose)

### Pasos para ejecutar

1. Clonar el repositorio:

   ```bash
   git clone <URL_DE_TU_REPOSITORIO>
   cd practica-bd-algebra
   ```

2. Construir y levantar los contenedores:

   ```bash
   docker-compose up -d --build
   ```

   Este comando:

   * Descarga la imagen de PostgreSQL
   * Construye la aplicación en Python
   * Inicializa automáticamente la base de datos

3. Ingresar al menú interactivo:

   ```bash
   docker attach universidad_menu
   ```

   *(Si el menú no aparece de inmediato, presiona ENTER una vez)*

4. Detener el sistema:

   ```bash
   docker-compose down
   ```

---

## 🧠 Consultas Implementadas

El sistema incluye **20 consultas**, clasificadas por tipo de operación:

| Categoría            | Operadores / Conceptos    | Descripción                                      |
| -------------------- | ------------------------- | ------------------------------------------------ |
| Operadores Básicos   | σ, π, ∪, ∩, −             | Selección, proyección y operaciones de conjuntos |
| Reuniones            | ⋈, ⟕, ▹, Self-Join        | Consultas con múltiples tablas                   |
| Agregación           | COUNT, SUM, AVG, GROUP BY | Estadísticas académicas                          |
| División             | ÷ (simulada)              | Consultas de totalidad                           |
| Lógica de Predicados | ∀, ∃                      | Cuantificadores universales y existenciales      |

Cada consulta se muestra en el menú con:

* Descripción en lenguaje natural
* Expresión en Álgebra Relacional
* Expresión en CRT y CRD
* Consulta SQL equivalente
* Resultado en pantalla

---

## 🎓 Equivalencias Teóricas

Este proyecto demuestra la traducción directa de operadores formales a SQL:

| Operador   | Símbolo | Concepto              | Implementación SQL |
| ---------- | ------- | --------------------- | ------------------ |
| Selección  | σ       | Filtrado de filas     | WHERE              |
| Proyección | π       | Selección de columnas | SELECT             |
| Reunión    | ⋈       | Combinación de tablas | JOIN               |
| Agrupación | γ       | Agrupar resultados    | GROUP BY           |
| División   | ÷       | "Para todo"           | NOT EXISTS         |
| Diferencia | −       | Resta de conjuntos    | EXCEPT             |

---

## 🛠 Tecnologías Utilizadas

* **PostgreSQL 15** – Sistema gestor de base de datos
* **Python 3** – Interfaz de línea de comandos (CLI)
* **psycopg2** – Conector PostgreSQL para Python
* **Docker & Docker Compose** – Contenerización
* **Git** – Control de versiones

---

## 🔧 Solución de Problemas Comunes

**Puerto 5432 ocupado**
Si PostgreSQL está instalado localmente, Docker puede fallar.

* Solución: Detener el servicio local o cambiar el puerto en `docker-compose.yml`.

**El menú no aparece**

* Presiona ENTER una vez después de `docker attach`.

**Error de conexión a la base de datos**

* Verifica que el contenedor de la base de datos esté activo con `docker ps`.

---

📌 **Fecha de entrega:** 19 de diciembre de 2025
✔️ **Modalidad B – Solo Repositorio**
