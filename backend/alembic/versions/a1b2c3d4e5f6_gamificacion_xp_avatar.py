"""gamificacion_xp_avatar

Revision ID: a1b2c3d4e5f6
Revises: 6629b5914636
Create Date: 2026-08-14 00:00:00.000001

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = '6629b5914636'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('perfil_gamificacion',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('perfil_alumno_id', sa.Integer(), nullable=False),
    sa.Column('xp', sa.Integer(), nullable=False),
    sa.Column('avatar_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.ForeignKeyConstraint(['perfil_alumno_id'], ['perfilalumno.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('perfil_alumno_id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('perfil_gamificacion')
