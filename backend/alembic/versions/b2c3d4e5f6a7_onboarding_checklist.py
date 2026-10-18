"""onboarding_checklist

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
Create Date: 2026-08-14 00:00:00.000002

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'b2c3d4e5f6a7'
down_revision: Union[str, Sequence[str], None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('progreso_onboarding',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('perfil_alumno_id', sa.Integer(), nullable=False),
    sa.Column('pasos_completados', sa.JSON(), nullable=False),
    sa.ForeignKeyConstraint(['perfil_alumno_id'], ['perfilalumno.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('perfil_alumno_id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('progreso_onboarding')
