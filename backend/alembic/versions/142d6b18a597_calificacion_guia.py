"""calificacion_guia

Revision ID: 142d6b18a597
Revises: 8ccac24900f8
Create Date: 2026-08-15 20:32:24.364042

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = '142d6b18a597'
down_revision: Union[str, Sequence[str], None] = '8ccac24900f8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('calificacion_guia',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('oa_id', sa.Integer(), nullable=False),
    sa.Column('perfil_alumno_id', sa.Integer(), nullable=False),
    sa.Column('estrellas', sa.Integer(), nullable=False),
    sa.Column('fecha', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['oa_id'], ['objetivo_aprendizaje.id'], ),
    sa.ForeignKeyConstraint(['perfil_alumno_id'], ['perfilalumno.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('oa_id', 'perfil_alumno_id', name='ix_calificacion_guia_oa_perfil')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('calificacion_guia')
