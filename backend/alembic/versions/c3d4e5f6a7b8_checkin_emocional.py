"""checkin_emocional

Revision ID: c3d4e5f6a7b8
Revises: b2c3d4e5f6a7
Create Date: 2026-08-14 00:00:00.000003

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'c3d4e5f6a7b8'
down_revision: Union[str, Sequence[str], None] = 'b2c3d4e5f6a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('registro_animo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('perfil_alumno_id', sa.Integer(), nullable=False),
    sa.Column('estado', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('fecha', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['perfil_alumno_id'], ['perfilalumno.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_registro_animo_perfil_fecha', 'registro_animo', ['perfil_alumno_id', 'fecha'], unique=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index('ix_registro_animo_perfil_fecha', table_name='registro_animo')
    op.drop_table('registro_animo')
