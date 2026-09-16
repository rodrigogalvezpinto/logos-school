"""orden_curricular_nivel

Revision ID: 30aa68132720
Revises: 32ad4dab694d
Create Date: 2026-08-15 17:00:17.257138

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '30aa68132720'
down_revision: Union[str, Sequence[str], None] = '32ad4dab694d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Orden curricular real, independiente del `id` (que en Desarrollo NO sigue este orden —
# ver el comentario en orm_models.py, Nivel.orden).
_ORDEN_POR_NOMBRE = {
    "1° básico": 1, "2° básico": 2, "3° básico": 3, "4° básico": 4,
    "5° básico": 5, "6° básico": 6, "7° básico": 7, "8° básico": 8,
    "1° medio": 9, "2° medio": 10, "3° medio": 11, "4° medio": 12,
}


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('nivel', sa.Column('orden', sa.Integer(), nullable=True))
    conexion = op.get_bind()
    tabla_nivel = sa.table('nivel', sa.column('id', sa.Integer), sa.column('nombre', sa.String), sa.column('orden', sa.Integer))
    for nombre, orden in _ORDEN_POR_NOMBRE.items():
        conexion.execute(tabla_nivel.update().where(tabla_nivel.c.nombre == nombre).values(orden=orden))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('nivel', 'orden')
