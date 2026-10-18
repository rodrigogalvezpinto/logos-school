"""Control de calidad de contenido (Fase 1, ítem 2.5.1 del plan de incorporación de
hallazgos de Brincus — ver planificacion/27-plan-incorporacion-hallazgos-brincus.md).

Wrapper de CLI sobre `app.application.contenido.validar_calidad.validar` — ver ese módulo
para la explicación completa de qué valida y por qué. Corre contra la base de datos real
(no la de test), igual que `qa_extraer_para_coherencia.py`.

Uso:
    cd backend && uv run python scripts/validar_calidad_contenido.py
Código de salida: 0 si no hay hallazgos, 1 si encontró algún problema.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlmodel import Session

from app.application.contenido.validar_calidad import validar
from app.infrastructure.persistence.db import engine


def main() -> int:
    with Session(engine) as session:
        hallazgos = validar(session)

    if not hallazgos:
        print("✔ Control de calidad de contenido: sin hallazgos.")
        return 0

    print(f"✘ Control de calidad de contenido: {len(hallazgos)} hallazgo(s):\n")
    for h in hallazgos:
        print(f"  - {h}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
