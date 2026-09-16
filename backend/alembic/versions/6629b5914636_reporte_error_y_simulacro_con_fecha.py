"""reporte_error_y_simulacro_con_fecha

Revision ID: 6629b5914636
Revises: 15c8ae38312c
Create Date: 2026-08-14 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '6629b5914636'
down_revision: Union[str, Sequence[str], None] = '15c8ae38312c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('conjunto_evaluacion', sa.Column('fecha_programada', sa.DateTime(), nullable=True))
    op.create_table('reporte_error',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tipo_contenido', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('contenido_id', sa.Integer(), nullable=False),
    sa.Column('perfil_alumno_id', sa.Integer(), nullable=False),
    sa.Column('comentario', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('fecha', sa.DateTime(), nullable=False),
    sa.Column('resuelto', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['perfil_alumno_id'], ['perfilalumno.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('reporte_error')
    op.drop_column('conjunto_evaluacion', 'fecha_programada')
