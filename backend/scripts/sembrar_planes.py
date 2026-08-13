"""Crea los 3 planes de pago reales definidos en planificacion/09-modelo-de-negocio.md.

Uso:
    python scripts/sembrar_planes.py

Idempotente: si un plan con ese nombre ya existe, se omite.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlmodel import Session, select

from app.infrastructure.persistence.db import engine, crear_tablas
from app.infrastructure.persistence.orm_models import Plan

PLANES = [
    {"nombre": "Mensual", "nivel_de_acceso": "completo", "precio_clp": 19990},
    {"nombre": "Por periodo de examinación", "nivel_de_acceso": "completo", "precio_clp": 89900},
    {"nombre": "Anual", "nivel_de_acceso": "completo", "precio_clp": 159900},
]


def main() -> None:
    crear_tablas()
    with Session(engine) as session:
        for datos in PLANES:
            existente = session.exec(select(Plan).where(Plan.nombre == datos["nombre"])).first()
            if existente:
                print(f"  {datos['nombre']}: ya existe, se omite.")
                continue
            session.add(Plan(**datos))
            session.commit()
            print(f"  {datos['nombre']}: creado (${datos['precio_clp']:,} CLP).".replace(",", "."))


if __name__ == "__main__":
    main()
