"""Seed del Plan Lector — piloto en 4° básico (ver
planificacion/25-analisis-competencia-brincus.md y planificacion/04-modo-de-operacion.md:
elegido con criterio pedagógico propio, no una lista arbitraria — libros reales, ampliamente
usados en colegios chilenos para esta edad, con dificultad de lectura apropiada a 4° básico).

Uso: python scripts/seed_plan_lector.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlmodel import Session, select

from app.infrastructure.persistence.db import engine
from app.infrastructure.persistence.orm_models import LibroPlanLector, Nivel

LIBROS_4_BASICO = [
    ("Papelucho", "Marcela Paz", "Editorial Planeta"),
    ("El Principito", "Antoine de Saint-Exupéry", "Editorial Salamandra"),
    ("Matilda", "Roald Dahl", "Alfaguara Infantil"),
    ("Charlie y la fábrica de chocolate", "Roald Dahl", "Alfaguara Infantil"),
]


def main() -> None:
    with Session(engine) as session:
        nivel = session.exec(select(Nivel).where(Nivel.nombre == "4° básico")).first()
        if not nivel:
            print("No se encontró el nivel 4° básico — importar el contenido primero.")
            return

        existentes = session.exec(select(LibroPlanLector).where(LibroPlanLector.nivel_id == nivel.id)).all()
        for libro in existentes:
            session.delete(libro)
        session.commit()

        for i, (titulo, autor, editorial) in enumerate(LIBROS_4_BASICO, start=1):
            session.add(LibroPlanLector(nivel_id=nivel.id, orden=i, titulo=titulo, autor=autor, editorial=editorial))
        session.commit()
        print(f"Plan Lector de 4° básico: {len(LIBROS_4_BASICO)} libros.")


if __name__ == "__main__":
    main()
