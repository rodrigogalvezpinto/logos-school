"""Seed de Útiles Escolares — piloto en 4° básico (ver
planificacion/25-analisis-competencia-brincus.md, Paso 12, sección "Informaciones": lista
real de materiales que un colegio chileno pide para este nivel, con criterio propio —
planificacion/04-modo-de-operacion.md — no inventada al azar).

Uso: python scripts/seed_utiles_escolares.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlmodel import Session, select

from app.infrastructure.persistence.db import engine
from app.infrastructure.persistence.orm_models import Nivel, UtilEscolar

# (nombre, cantidad, asignatura) — asignatura=None cuando el útil es general, no de una
# materia puntual (ej. estuche, block).
UTILES_4_BASICO = [
    ("Cuaderno universitario cuadro grande", "1", "Matemática"),
    ("Cuaderno universitario cuadro grande", "1", "Lenguaje y Comunicación"),
    ("Cuaderno universitario cuadro grande", "1", "Ciencias Naturales"),
    ("Cuaderno universitario cuadro grande", "1", "Historia, Geografía y Cs. Sociales"),
    ("Estuche completo (lápices grafito, goma, sacapuntas, lápices de colores)", "1", None),
    ("Regla de 20 cm", "1", "Matemática"),
    ("Block de dibujo tamaño 99", "1", None),
    ("Diccionario de español para niños", "1", "Lenguaje y Comunicación"),
    ("Calculadora básica", "1", "Matemática"),
    ("Carpeta con archivador", "4", None),
]


def main() -> None:
    with Session(engine) as session:
        nivel = session.exec(select(Nivel).where(Nivel.nombre == "4° básico")).first()
        if not nivel:
            print("No se encontró el nivel 4° básico — importar el contenido primero.")
            return

        existentes = session.exec(select(UtilEscolar).where(UtilEscolar.nivel_id == nivel.id)).all()
        for util in existentes:
            session.delete(util)
        session.commit()

        for i, (nombre, cantidad, asignatura) in enumerate(UTILES_4_BASICO, start=1):
            session.add(
                UtilEscolar(nivel_id=nivel.id, orden=i, nombre=nombre, cantidad=cantidad, asignatura=asignatura)
            )
        session.commit()
        print(f"Útiles Escolares de 4° básico: {len(UTILES_4_BASICO)} ítems.")


if __name__ == "__main__":
    main()
