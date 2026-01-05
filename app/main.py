import os
import time
import psycopg2
from tabulate import tabulate

def get_connection():
    max_retries = 20
    for i in range(max_retries):
        try:
            conn = psycopg2.connect(
                host=os.getenv('DB_HOST', 'db'),
                database=os.getenv('DB_NAME', 'algebra_db'),
                user=os.getenv('DB_USER', 'user'),
                password=os.getenv('DB_PASS', 'password')
            )
            return conn
        except psycopg2.OperationalError:
            print(f"Esperando a la BD... ({i+1}/{max_retries})")
            time.sleep(2)
    raise Exception("Error de conexion")


consultas = [
    # --- GRUPO 1: OPERADORES BÁSICOS (5) ---
    {
        "id": 1,
        "tipo": "Selección (σ)",
        "descripcion": "Estudiantes del departamento 'ISC'",
        "ar": "σ id_depto='ISC' (ESTUDIANTES)",
        "crt": "{t | ESTUDIANTES(t) ∧ t.id_depto = 'ISC'}",
        "crd": "{<id,n,e,g,d> | <id,n,e,g,d> ∈ ESTUDIANTES ∧ d = 'ISC'}",
        "sql": "SELECT * FROM estudiantes WHERE id_depto = 'ISC';"
    },
    {
        "id": 2,
        "tipo": "Proyección (π)",
        "descripcion": "Nombre y Salario de profesores (> 40000)",
        "ar": "π nombre, salario (σ salario > 40000 (PROFESORES))",
        "crt": "{t.nombre, t.salario | PROFESORES(t) ∧ t.salario > 40000}",
        "crd": "{<n, s> | ∃id, g, d (<id, n, g, s, d> ∈ PROFESORES ∧ s > 40000)}",
        "sql": "SELECT nombre, salario FROM profesores WHERE salario > 40000;"
    },
    {
        "id": 3,
        "tipo": "Unión (∪)",
        "descripcion": "Lista unificada de Correos de Estudiantes y Profesores",
        "ar": "π email (ESTUDIANTES) ∪ π email (PROFESORES)",
        "crt": "{t.email | ESTUDIANTES(t) ∨ PROFESORES(t)}",
        "crd": "{<e> | ∃id, n, g, d (<id,n,e,g,d> ∈ ESTUDIANTES) ∨ ∃id, n, g, s, d (<id,n,g,s,d> ∈ PROFESORES)}",
        "sql": "SELECT email FROM estudiantes UNION SELECT email FROM profesores;"
    },
    {
        "id": 4,
        "tipo": "Diferencia (-)",
        "descripcion": "Cursos que NO tienen prerrequisitos asignados",
        "ar": "π id_curso (CURSOS) - π id_curso (PRERREQUISITOS)",
        "crt": "{c.id_curso | CURSOS(c) ∧ ¬∃p(PRERREQUISITOS(p) ∧ p.id_curso = c.id_curso)}",
        "crd": "{<id> | <id,n,c,s,d> ∈ CURSOS ∧ ¬∃r,t,f (<id,r,t,f> ∈ PRERREQUISITOS)}",
        "sql": "SELECT id_curso FROM cursos EXCEPT SELECT id_curso FROM prerrequisitos;"
    },
    {
        "id": 5,
        "tipo": "Producto Cartesiano (×)",
        "descripcion": "Todas las combinaciones posibles de Estudiantes y Cursos (Muestra 5)",
        "ar": "ESTUDIANTES × CURSOS",
        "crt": "{e, c | ESTUDIANTES(e) ∧ CURSOS(c)}",
        "crd": "{<e_attr, c_attr> | <e_attr> ∈ ESTUDIANTES ∧ <c_attr> ∈ CURSOS}",
        "sql": "SELECT e.nombre, c.nombre FROM estudiantes e CROSS JOIN cursos c LIMIT 5;"
    },

    # --- GRUPO 2: REUNIONES (5) ---
    {
        "id": 6,
        "tipo": "Reunión Natural (⋈)",
        "descripcion": "Estudiantes y sus calificaciones (Join de 3 tablas)",
        "ar": "π nombre, calificacion (ESTUDIANTES ⋈ INSCRIPCIONES ⋈ GRUPOS)",
        "crt": "{e.nombre, i.calificacion | ∃g(EST(e) ∧ INS(i) ∧ GRP(g) ∧ e.id=i.id ∧ i.idg=g.idg)}",
        "crd": "Equivalente a Join por claves foráneas",
        "sql": """
        SELECT e.nombre, c.nombre as materia, i.calificacion 
        FROM estudiantes e 
        JOIN inscripciones i ON e.id_est = i.id_est
        JOIN grupos g ON i.id_grupo = g.id_grupo
        JOIN cursos c ON g.id_curso = c.id_curso;
        """
    },
    {
        "id": 7,
        "tipo": "Left Outer Join (⟕)",
        "descripcion": "Todos los Deptos, incluso sin estudiantes",
        "ar": "DEPARTAMENTOS ⟕ ESTUDIANTES",
        "crt": "Requiere manejo explícito de valores NULL",
        "crd": "Requiere manejo explícito de valores NULL",
        "sql": """
        SELECT d.nombre, e.nombre as estudiante
        FROM departamentos d
        LEFT JOIN estudiantes e ON d.id_depto = e.id_depto;
        """
    },
    {
        "id": 8,
        "tipo": "Theta Join (⋈_θ)",
        "descripcion": "Grupos impartidos por profesores con salario > 40000",
        "ar": "GRUPOS ⋈_(prof.salario > 40000) PROFESORES",
        "crt": "{g, p | GRUPOS(g) ∧ PROFESORES(p) ∧ g.id_prof = p.id_prof ∧ p.salario > 40000}",
        "crd": "...",
        "sql": """
        SELECT g.id_grupo, p.nombre, p.salario 
        FROM grupos g 
        JOIN profesores p ON g.id_prof = p.id_prof 
        WHERE p.salario > 40000;
        """
    },
    {
        "id": 9,
        "tipo": "Semi-Join (⋉) (EXISTS)",
        "descripcion": "Estudiantes que tienen al menos una inscripción",
        "ar": "ESTUDIANTES ⋉ INSCRIPCIONES",
        "crt": "{e | ESTUDIANTES(e) ∧ ∃i(INSCRIPCIONES(i) ∧ e.id = i.id)}",
        "crd": "...",
        "sql": """
        SELECT nombre FROM estudiantes e 
        WHERE EXISTS (SELECT 1 FROM inscripciones i WHERE i.id_est = e.id_est);
        """
    },
    {
        "id": 10,
        "tipo": "Self Join (Auto-Reunión)",
        "descripcion": "Pares de estudiantes de la misma generación",
        "ar": "ρ(E1, EST) ⋈_(E1.gen=E2.gen) ρ(E2, EST)",
        "crt": "{e1.nom, e2.nom | EST(e1) ∧ EST(e2) ∧ e1.gen = e2.gen ∧ e1.id < e2.id}",
        "crd": "...",
        "sql": """
        SELECT e1.nombre, e2.nombre, e1.generacion
        FROM estudiantes e1
        JOIN estudiantes e2 ON e1.generacion = e2.generacion
        WHERE e1.id_est < e2.id_est
        LIMIT 10;
        """
    },

    # --- GRUPO 3: AGRUPACIÓN Y AGREGACIÓN (5) ---
    {
        "id": 11,
        "tipo": "Agrupación (γ AVG)",
        "descripcion": "Promedio de salario por departamento",
        "ar": "id_depto ℑ avg(salario) (PROFESORES)",
        "crt": "No soportado en CRT estándar",
        "crd": "No soportado en CRD estándar",
        "sql": "SELECT id_depto, AVG(salario) FROM profesores GROUP BY id_depto;"
    },
    {
        "id": 12,
        "tipo": "Agrupación (γ COUNT)",
        "descripcion": "Número de estudiantes por departamento",
        "ar": "id_depto ℑ count(id_est) (ESTUDIANTES)",
        "crt": "No soportado",
        "crd": "No soportado",
        "sql": "SELECT id_depto, COUNT(*) FROM estudiantes GROUP BY id_depto;"
    },
    {
        "id": 13,
        "tipo": "Agrupación con Condición (HAVING)",
        "descripcion": "Departamentos con presupuesto total > 1,000,000 (Suma)",
        "ar": "σ sum_pres > 1000000 (id_depto ℑ sum(presupuesto) (DEPTOS))",
        "crt": "No soportado",
        "crd": "No soportado",
        "sql": "SELECT edificio, SUM(presupuesto) FROM departamentos GROUP BY edificio HAVING SUM(presupuesto) > 1000000;"
    },
    {
        "id": 14,
        "tipo": "Agregación (MAX)",
        "descripcion": "La calificación más alta registrada en inscripciones",
        "ar": "ℑ max(calificacion) (INSCRIPCIONES)",
        "crt": "No soportado",
        "crd": "No soportado",
        "sql": "SELECT MAX(calificacion) as Nota_Maxima FROM inscripciones;"
    },
    {
        "id": 15,
        "tipo": "Agregación (COUNT DISTINCT)",
        "descripcion": "Cuántos departamentos distintos tienen cursos asignados",
        "ar": "ℑ count_distinct(id_depto) (CURSOS)",
        "crt": "No soportado",
        "crd": "No soportado",
        "sql": "SELECT COUNT(DISTINCT id_depto) FROM cursos;"
    },

    # --- GRUPO 4: DIVISIÓN (3) ---
    {
        "id": 16,
        "tipo": "División (÷) - Caso 1",
        "descripcion": "Estudiantes que han tomado TODOS los cursos de 'IA'",
        "ar": "π id_est, id_curso (INSCRIPCIONES_VISTA) ÷ π id_curso (σ id_depto='IA'(CURSOS))",
        "crt": "{e | EST(e) ∧ ∀c ((CUR(c) ∧ c.depto='IA') → ∃i (INS(i) ∧ i.id_est=e.id ∧ i.curso=c.id))}",
        "crd": "...",
        "sql": """
        SELECT e.nombre FROM estudiantes e
        WHERE NOT EXISTS (
            SELECT id_curso FROM cursos WHERE id_depto = 'IA'
            EXCEPT
            SELECT g.id_curso FROM inscripciones i 
            JOIN grupos g ON i.id_grupo = g.id_grupo
            WHERE i.id_est = e.id_est
        );
        """
    },
    {
        "id": 17,
        "tipo": "División (÷) - Caso 2",
        "descripcion": "Estudiantes que han tomado TODOS los cursos de Ciencias Básicas (BAS)",
        "ar": "π id_est, id_curso (VISTA) ÷ π id_curso (σ id_depto='BAS'(CURSOS))",
        "crt": "Similar al anterior pero con depto='BAS'",
        "crd": "...",
        "sql": """
        SELECT e.nombre FROM estudiantes e
        WHERE NOT EXISTS (
            SELECT id_curso FROM cursos WHERE id_depto = 'BAS'
            EXCEPT
            SELECT g.id_curso FROM inscripciones i 
            JOIN grupos g ON i.id_grupo = g.id_grupo
            WHERE i.id_est = e.id_est
        );
        """
    },
    {
        "id": 18,
        "tipo": "División (÷) - Caso 3",
        "descripcion": "Profesores que han impartido clases en TODAS las aulas de tipo 'Laboratorio' (Simulado)",
        "ar": "π id_prof, id_aula (GRUPOS) ÷ π id_aula (σ tipo='Laboratorio'(AULAS))",
        "crt": "...",
        "crd": "...",
        "sql": """
        SELECT p.nombre FROM profesores p
        WHERE NOT EXISTS (
            SELECT id_aula FROM aulas WHERE tipo = 'Laboratorio'
            EXCEPT
            SELECT id_aula FROM grupos g WHERE g.id_prof = p.id_prof
        );
        """
    },

    # --- GRUPO 5: CUANTIFICADORES UNIVERSALES (2) ---
    {
        "id": 19,
        "tipo": "Cuantificador Universal (∀)",
        "descripcion": "Departamentos donde TODOS sus profesores tienen grado de 'Doctorado'",
        "ar": "DEPTOS - π id_depto (σ grado ≠ 'Doctorado' (PROFESORES))",
        "crt": "{d.nombre | DEPTOS(d) ∧ ∀p (PROFESORES(p) ∧ p.id_depto = d.id_depto → p.grado = 'Doctorado')}",
        "crd": "...",
        "sql": """
        SELECT nombre FROM departamentos d
        WHERE NOT EXISTS (
            SELECT 1 FROM profesores p 
            WHERE p.id_depto = d.id_depto AND p.grado_academico != 'Doctorado'
        );
        """
    },
    {
        "id": 20,
        "tipo": "Cuantificador Universal (∀)",
        "descripcion": "Estudiantes que han aprobado (>=6) TODAS sus materias inscritas",
        "ar": "ESTUDIANTES - π id_est (σ calificacion < 6 (INSCRIPCIONES))",
        "crt": "{e.nombre | EST(e) ∧ ∀i (INS(i) ∧ i.id_est = e.id → i.calificacion >= 6)}",
        "crd": "...",
        "sql": """
        SELECT nombre FROM estudiantes e
        WHERE NOT EXISTS (
            SELECT 1 FROM inscripciones i 
            WHERE i.id_est = e.id_est AND i.calificacion < 6.0
        ) AND EXISTS (SELECT 1 FROM inscripciones i WHERE i.id_est = e.id_est);
        """
    }
]

def ejecutar_consulta(conn, consulta):
    print("\n" + "="*80)
    print(f"CONSULTA {consulta['id']}: {consulta['descripcion']}")
    print("-" * 80)
    print(f"1. Álgebra Relacional:       {consulta['ar']}")
    print(f"2. Cálculo Relacional Tuplas:{consulta['crt']}")
    print(f"3. Cálculo Relacional Dom:   {consulta['crd']}")
    print(f"4. SQL Equivalente:          \n{consulta['sql']}")
    print("-" * 80)
    print("RESULTADO:")
    try:
        cur = conn.cursor()
        cur.execute(consulta['sql'])
        if cur.description:
            headers = [desc[0] for desc in cur.description]
            rows = cur.fetchall()
            print(tabulate(rows, headers=headers, tablefmt="psql"))
        else:
            print("Operación exitosa.")
        cur.close()
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    input("\nPresiona ENTER...")

def menu():
    conn = get_connection()
    while True:
        os.system('clear')
        print("=== PRACTICA 6, 7 Y 8: Operaciones del Álgebra Relacional ===")
        print("--- Básicas ---")
        for c in consultas[:5]: print(f"{c['id']}. {c['tipo']}")
        print("--- Reuniones ---")
        for c in consultas[5:10]: print(f"{c['id']}. {c['tipo']}")
        print("--- Agregación ---")
        for c in consultas[10:15]: print(f"{c['id']}. {c['tipo']}")
        print("--- División ---")
        for c in consultas[15:18]: print(f"{c['id']}. {c['tipo']}")
        print("--- Cuantificadores ---")
        for c in consultas[18:]: print(f"{c['id']}. {c['tipo']}")
        
        print("\n0. Salir")
        op = input("Selección: ")
        if op == '0': break
        sel = next((c for c in consultas if str(c['id']) == op), None)
        if sel: ejecutar_consulta(conn, sel)

if __name__ == "__main__":
    menu()