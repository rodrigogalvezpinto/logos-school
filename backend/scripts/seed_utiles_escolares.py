"""Seed de Útiles Escolares, de 1.° básico a 4.° medio (piloto en 4.° básico: 2026-08-15; los 12 cursos: 2026-11-22).

Lista sugerida de materiales para estudiar en casa el temario de cada curso, con las asignaturas de su examen
(criterio propio, planificacion/04-modo-de-operacion.md). Es una guía, no una exigencia del Examen Libre.
Idempotente: reemplaza la lista de cada nivel.

Uso: python scripts/seed_utiles_escolares.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlmodel import Session, select

from app.infrastructure.persistence.db import engine
from app.infrastructure.persistence.orm_models import Nivel, UtilEscolar

# nivel -> [(nombre, cantidad, asignatura)]; asignatura=None cuando el útil es general.
UTILES = {'1° básico': [('Cuaderno college caligrafía horizontal, 100 hojas', '1', 'Lenguaje y Comunicación'),
               ('Cuaderno college cuadro grande (7 mm), 100 hojas', '1', 'Matemática'),
               ('Cuaderno college cuadro grande (7 mm), 60 hojas', '1', 'Ciencias Naturales'),
               ('Cuaderno college cuadro grande (7 mm), 60 hojas', '1', 'Historia, Geografía y Cs. Sociales'),
               ('Estuche con lápices grafito, goma, sacapuntas con depósito y lápices de colores', '1', None),
               ('Regla de 20 cm', '1', 'Matemática'),
               ('Material concreto para contar (palos de helado, fichas o porotos)', '1 bolsa', 'Matemática'),
               ('Block de dibujo tamaño 99', '1', None),
               ('Pegamento en barra y tijera punta roma', '1', None),
               ('Carpeta plastificada con acoclip para guías', '1', None)],
 '2° básico': [('Cuaderno college caligrafía horizontal, 100 hojas', '1', 'Lenguaje y Comunicación'),
               ('Cuaderno college cuadro grande (7 mm), 100 hojas', '1', 'Matemática'),
               ('Cuaderno college cuadro grande (7 mm), 60 hojas', '1', 'Ciencias Naturales'),
               ('Cuaderno college cuadro grande (7 mm), 60 hojas', '1', 'Historia, Geografía y Cs. Sociales'),
               ('Estuche con lápices grafito, goma, sacapuntas con depósito y lápices de colores', '1', None),
               ('Regla de 20 cm', '1', 'Matemática'),
               ('Material concreto para contar (palos de helado, fichas o porotos)', '1 bolsa', 'Matemática'),
               ('Block de dibujo tamaño 99', '1', None),
               ('Pegamento en barra y tijera punta roma', '1', None),
               ('Carpeta plastificada con acoclip para guías', '1', None)],
 '3° básico': [('Cuaderno college cuadro grande (7 mm), 100 hojas', '1', 'Lenguaje y Comunicación'),
               ('Cuaderno college cuadro grande (7 mm), 100 hojas', '1', 'Matemática'),
               ('Cuaderno college cuadro grande (7 mm), 60 hojas', '1', 'Ciencias Naturales'),
               ('Cuaderno college cuadro grande (7 mm), 60 hojas', '1', 'Historia, Geografía y Cs. Sociales'),
               ('Estuche con lápices grafito, goma, sacapuntas y lápices de colores', '1', None),
               ('Regla de 20 cm', '1', 'Matemática'),
               ('Diccionario de español escolar', '1', 'Lenguaje y Comunicación'),
               ('Atlas escolar de Chile y el mundo', '1', 'Historia, Geografía y Cs. Sociales'),
               ('Block de dibujo tamaño 99', '1', None),
               ('Carpeta plastificada con acoclip para guías', '1', None)],
 '4° básico': [('Cuaderno universitario cuadro grande, 100 hojas', '1', 'Lenguaje y Comunicación'),
               ('Cuaderno universitario cuadro grande, 100 hojas', '1', 'Matemática'),
               ('Cuaderno universitario cuadro grande, 100 hojas', '1', 'Ciencias Naturales'),
               ('Cuaderno universitario cuadro grande, 100 hojas', '1', 'Historia, Geografía y Cs. Sociales'),
               ('Estuche con lápices grafito, goma, sacapuntas y lápices de colores', '1', None),
               ('Regla de 20 cm y transportador', '1', 'Matemática'),
               ('Diccionario de español escolar', '1', 'Lenguaje y Comunicación'),
               ('Atlas escolar de Chile y el mundo', '1', 'Historia, Geografía y Cs. Sociales'),
               ('Block de dibujo tamaño 99', '1', None),
               ('Carpeta con archivador para guías', '1', None)],
 '5° básico': [('Cuaderno universitario cuadro grande, 100 hojas', '1', 'Lenguaje y Comunicación'),
               ('Cuaderno universitario cuadro grande, 100 hojas', '1', 'Matemática'),
               ('Cuaderno universitario cuadro grande, 100 hojas', '1', 'Ciencias Naturales'),
               ('Cuaderno universitario cuadro grande, 100 hojas', '1', 'Historia, Geografía y Cs. Sociales'),
               ('Cuaderno universitario cuadro grande, 60 hojas', '1', 'Inglés'),
               ('Estuche con lápiz grafito, lápiz pasta azul y rojo, goma, sacapuntas y destacador', '1', None),
               ('Set de geometría: regla de 30 cm, escuadra y transportador', '1', 'Matemática'),
               ('Compás', '1', 'Matemática'),
               ('Diccionario de español escolar', '1', 'Lenguaje y Comunicación'),
               ('Diccionario inglés-español', '1', 'Inglés'),
               ('Atlas escolar de Chile y el mundo', '1', 'Historia, Geografía y Cs. Sociales'),
               ('Carpeta con archivador para guías', '1', None)],
 '6° básico': [('Cuaderno universitario cuadro grande, 100 hojas', '1', 'Lenguaje y Comunicación'),
               ('Cuaderno universitario cuadro grande, 100 hojas', '1', 'Matemática'),
               ('Cuaderno universitario cuadro grande, 100 hojas', '1', 'Ciencias Naturales'),
               ('Cuaderno universitario cuadro grande, 100 hojas', '1', 'Historia, Geografía y Cs. Sociales'),
               ('Cuaderno universitario cuadro grande, 60 hojas', '1', 'Inglés'),
               ('Estuche con lápiz grafito, lápiz pasta azul y rojo, goma, sacapuntas y destacador', '1', None),
               ('Set de geometría: regla de 30 cm, escuadra y transportador', '1', 'Matemática'),
               ('Compás', '1', 'Matemática'),
               ('Diccionario de español escolar', '1', 'Lenguaje y Comunicación'),
               ('Diccionario inglés-español', '1', 'Inglés'),
               ('Atlas escolar de Chile y el mundo', '1', 'Historia, Geografía y Cs. Sociales'),
               ('Carpeta con archivador para guías', '1', None)],
 '7° básico': [('Cuaderno universitario cuadro grande, 100 hojas', '1', 'Lengua y Literatura'),
               ('Cuaderno universitario cuadro grande, 100 hojas', '1', 'Matemática'),
               ('Cuaderno universitario cuadro grande, 100 hojas', '1', 'Ciencias Naturales'),
               ('Cuaderno universitario cuadro grande, 100 hojas', '1', 'Historia, Geografía y Cs. Sociales'),
               ('Cuaderno universitario cuadro grande, 60 hojas', '1', 'Inglés'),
               ('Estuche con lápiz grafito, lápiz pasta azul y rojo, goma, sacapuntas y destacador', '1', None),
               ('Set de geometría: regla de 30 cm, escuadra y transportador', '1', 'Matemática'),
               ('Compás', '1', 'Matemática'),
               ('Diccionario de español escolar', '1', 'Lengua y Literatura'),
               ('Diccionario inglés-español', '1', 'Inglés'),
               ('Atlas escolar de Chile y el mundo', '1', 'Historia, Geografía y Cs. Sociales'),
               ('Carpeta con archivador para guías', '1', None),
               ('Calculadora básica', '1', 'Matemática')],
 '8° básico': [('Cuaderno universitario cuadro grande, 100 hojas', '1', 'Lengua y Literatura'),
               ('Cuaderno universitario cuadro grande, 100 hojas', '1', 'Matemática'),
               ('Cuaderno universitario cuadro grande, 100 hojas', '1', 'Ciencias Naturales'),
               ('Cuaderno universitario cuadro grande, 100 hojas', '1', 'Historia, Geografía y Cs. Sociales'),
               ('Cuaderno universitario cuadro grande, 60 hojas', '1', 'Inglés'),
               ('Estuche con lápiz grafito, lápiz pasta azul y rojo, goma, sacapuntas y destacador', '1', None),
               ('Set de geometría: regla de 30 cm, escuadra y transportador', '1', 'Matemática'),
               ('Compás', '1', 'Matemática'),
               ('Diccionario de español escolar', '1', 'Lengua y Literatura'),
               ('Diccionario inglés-español', '1', 'Inglés'),
               ('Atlas escolar de Chile y el mundo', '1', 'Historia, Geografía y Cs. Sociales'),
               ('Carpeta con archivador para guías', '1', None),
               ('Calculadora científica', '1', 'Matemática')],
 '1° medio': [('Cuaderno universitario cuadro grande, 100 hojas', '1', 'Lengua y Literatura'),
              ('Cuaderno universitario cuadro grande, 100 hojas', '1', 'Matemática'),
              ('Cuaderno universitario cuadro grande, 100 hojas', '1', 'Ciencias Naturales'),
              ('Cuaderno universitario cuadro grande, 100 hojas', '1', 'Historia, Geografía y Cs. Sociales'),
              ('Cuaderno universitario cuadro grande, 100 hojas', '1', 'Inglés'),
              ('Estuche con lápiz grafito, lápices pasta, goma, corrector y destacadores', '1', None),
              ('Calculadora científica', '1', 'Matemática'),
              ('Set de geometría: regla de 30 cm, escuadra, transportador y compás', '1', 'Matemática'),
              ('Diccionario inglés-español', '1', 'Inglés'),
              ('Carpeta con archivador o fundas para guías y ensayos', '1', None)],
 '2° medio': [('Cuaderno universitario cuadro grande, 100 hojas', '1', 'Lengua y Literatura'),
              ('Cuaderno universitario cuadro grande, 100 hojas', '1', 'Matemática'),
              ('Cuaderno universitario cuadro grande, 100 hojas', '1', 'Ciencias Naturales'),
              ('Cuaderno universitario cuadro grande, 100 hojas', '1', 'Historia, Geografía y Cs. Sociales'),
              ('Cuaderno universitario cuadro grande, 100 hojas', '1', 'Inglés'),
              ('Estuche con lápiz grafito, lápices pasta, goma, corrector y destacadores', '1', None),
              ('Calculadora científica', '1', 'Matemática'),
              ('Set de geometría: regla de 30 cm, escuadra, transportador y compás', '1', 'Matemática'),
              ('Diccionario inglés-español', '1', 'Inglés'),
              ('Carpeta con archivador o fundas para guías y ensayos', '1', None)],
 '3° medio': [('Cuaderno universitario cuadro grande, 100 hojas', '1', 'Lengua y Literatura'),
              ('Cuaderno universitario cuadro grande, 100 hojas', '1', 'Matemática'),
              ('Cuaderno universitario cuadro grande, 100 hojas', '1', 'Ciencias para la Ciudadanía'),
              ('Cuaderno universitario cuadro grande, 100 hojas', '1', 'Filosofía'),
              ('Cuaderno universitario cuadro grande, 100 hojas', '1', 'Inglés'),
              ('Cuaderno universitario cuadro grande, 100 hojas', '1', 'Educación Ciudadana'),
              ('Estuche con lápiz grafito, lápices pasta, goma, corrector y destacadores', '1', None),
              ('Calculadora científica', '1', 'Matemática'),
              ('Set de geometría: regla de 30 cm, escuadra, transportador y compás', '1', 'Matemática'),
              ('Diccionario inglés-español', '1', 'Inglés'),
              ('Carpeta con archivador o fundas para guías y ensayos', '1', None)],
 '4° medio': [('Cuaderno universitario cuadro grande, 100 hojas', '1', 'Lengua y Literatura'),
              ('Cuaderno universitario cuadro grande, 100 hojas', '1', 'Matemática'),
              ('Cuaderno universitario cuadro grande, 100 hojas', '1', 'Ciencias para la Ciudadanía'),
              ('Cuaderno universitario cuadro grande, 100 hojas', '1', 'Filosofía'),
              ('Cuaderno universitario cuadro grande, 100 hojas', '1', 'Inglés'),
              ('Cuaderno universitario cuadro grande, 100 hojas', '1', 'Educación Ciudadana'),
              ('Estuche con lápiz grafito, lápices pasta, goma, corrector y destacadores', '1', None),
              ('Calculadora científica', '1', 'Matemática'),
              ('Set de geometría: regla de 30 cm, escuadra, transportador y compás', '1', 'Matemática'),
              ('Diccionario inglés-español', '1', 'Inglés'),
              ('Carpeta con archivador o fundas para guías y ensayos', '1', None)]}


def main() -> None:
    with Session(engine) as session:
        total = 0
        for nombre_nivel, utiles in UTILES.items():
            nivel = session.exec(select(Nivel).where(Nivel.nombre == nombre_nivel)).first()
            if not nivel:
                print(f"No se encontró el nivel {nombre_nivel} — importar el contenido primero.")
                continue
            for util in session.exec(select(UtilEscolar).where(UtilEscolar.nivel_id == nivel.id)).all():
                session.delete(util)
            session.commit()
            for i, (nombre, cantidad, asignatura) in enumerate(utiles, start=1):
                session.add(UtilEscolar(nivel_id=nivel.id, orden=i, nombre=nombre, cantidad=cantidad, asignatura=asignatura))
            session.commit()
            total += len(utiles)
        print(f"Útiles Escolares: {total} ítems en {len(UTILES)} cursos.")


if __name__ == "__main__":
    main()
