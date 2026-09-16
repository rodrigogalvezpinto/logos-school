"""plan_lector

Revision ID: d935d005f145
Revises: c3d4e5f6a7b8
Create Date: 2026-08-15 15:54:43.687333

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = 'd935d005f145'
down_revision: Union[str, Sequence[str], None] = 'c3d4e5f6a7b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Solo la tabla nueva del Plan Lector — el autogenerate también detectó un cambio de
    # nullability en progreso_onboarding.pasos_completados, drift preexistente no
    # relacionado con este cambio, se deja fuera para mantener esta migración acotada.
    op.create_table('libro_plan_lector',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nivel_id', sa.Integer(), nullable=False),
    sa.Column('orden', sa.Integer(), nullable=False),
    sa.Column('titulo', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('autor', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('editorial', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.ForeignKeyConstraint(['nivel_id'], ['nivel.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('libro_plan_lector')
