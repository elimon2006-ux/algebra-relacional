# Sistema Universitario: Álgebra Relacional y SQL

**Proyecto Final - Bases de Datos** *Escuela Superior de Cómputo (ESCOM - IPN)*

Este repositorio contiene la implementación de un **Caso Integrador** para la materia de Bases de Datos. El proyecto modela un sistema de gestión universitaria y demuestra la equivalencia entre cuatro lenguajes de consulta: **Álgebra Relacional**, **Cálculo Relacional de Tuplas**, **Cálculo Relacional de Dominios** y **SQL**.

---

## 👥 Integrantes del Equipo

* **González Estrada Naomi**
* **Herrera Zaragoza Elizabeth**
* **Romero Diego**
* **Grupo:** 3CV2

---

## 🏛️ Descripción del Dominio

El sistema modela la información académica de una universidad, gestionando:
* **Departamentos:** Entidades administrativas (ej. Sistemas, IA, Básicas).
* **Profesores y Estudiantes:** Vinculados a departamentos.
* **Cursos y Prerrequisitos:** Malla curricular y seriación.
* **Grupos y Aulas:** Programación académica (horarios y espacios físicos).
* **Inscripciones:** Historial académico y calificaciones.

El objetivo principal es ejecutar consultas de alta complejidad (incluyendo **División Relacional** y **Cuantificadores Universales**) mediante un menú interactivo.

---

## 📊 Diagrama Entidad-Relación Extendido (EER)

El siguiente diagrama ilustra la estructura de la base de datos y las relaciones entre las entidades (Cardinalidad y Foreign Keys).

```mermaid
erDiagram
    DEPARTAMENTOS ||--|{ PROFESORES : emplea
    DEPARTAMENTOS ||--|{ ESTUDIANTES : inscribe
    DEPARTAMENTOS ||--|{ CURSOS : oferta
    
    CURSOS ||--|{ GRUPOS : programa
    CURSOS ||--|{ PRERREQUISITOS : requiere
    
    PROFESORES ||--|{ GRUPOS : imparte
    
    AULAS ||--|{ GRUPOS : aloja
    
    ESTUDIANTES ||--|{ INSCRIPCIONES : cursa
    GRUPOS ||--|{ INSCRIPCIONES : tiene

    DEPARTAMENTOS {
        string id_depto PK
        string nombre
        decimal presupuesto
        string edificio
    }

    ESTUDIANTES {
        int id_est PK
        string nombre
        string email
        int generacion
        string id_depto FK
    }

    PROFESORES {
        int id_prof PK
        string nombre
        string grado
        decimal salario
        string id_depto FK
    }

    CURSOS {
        string id_curso PK
        string nombre
        int creditos
        string id_depto FK
    }

    GRUPOS {
        int id_grupo PK
        string id_curso FK
        int id_prof FK
        string id_aula FK
        string semestre
    }

    INSCRIPCIONES {
        int id_est PK,FK
        int id_grupo PK,FK
        decimal calificacion
    }

    🚀 Instalación y Ejecución
Este proyecto está Dockerizado para facilitar su despliegue sin necesidad de configurar PostgreSQL o Python manualmente.

Prerrequisitos
Tener instalado Docker Desktop y Docker Compose.

Pasos para ejecutar
Clonar o descargar este repositorio.

Abrir una terminal en la carpeta raíz del proyecto.

Ejecutar el siguiente comando para construir los contenedores y cargar la base de datos:

Bash

docker-compose up --build
Acceder al Menú Interactivo: Una vez que veas que la base de datos se ha iniciado, abre una nueva terminal y ejecuta:

Bash

docker attach practica-bd-algebra-app-1
(Nota: Si no ves el menú inmediatamente, presiona ENTER una vez).

📂 Estructura del Proyecto
app/main.py: Código fuente en Python. Contiene el menú interactivo y la definición de las 20 consultas con sus expresiones matemáticas.

db/init.sql: Script SQL. Crea las 8 tablas e inserta más de 100 tuplas de datos de prueba automáticamente al iniciar.

Dockerfile: Define el entorno de Python con las librerías necesarias (psycopg2, tabulate).

docker-compose.yml: Orquesta los servicios de la Base de Datos (Postgres) y la Aplicación (Python).

📝 Catálogo de Consultas
El sistema permite ejecutar 20 consultas complejas clasificadas en 5 categorías, cumpliendo con la rúbrica de evaluación:

Operadores Básicos: Selección, Proyección, Unión, Diferencia, Producto Cartesiano.

Reuniones (Joins): Natural Join, Left Join, Theta Join, Semi-Join, Self-Join.

Agregación y Agrupación: GROUP BY, HAVING, Promedios, Conteos.

División Relacional (÷):

Ejemplo: "Estudiantes que han tomado TODOS los cursos del área de Inteligencia Artificial".

Cuantificadores Universales (∀):

Ejemplo: "Estudiantes que han aprobado todas sus materias".

Cada resultado muestra en pantalla:

Expresión en Álgebra Relacional.

Expresión en Cálculo Relacional de Tuplas.

Expresión en Cálculo Relacional de Dominios.

Consulta SQL equivalente.

Tabla de Resultados.