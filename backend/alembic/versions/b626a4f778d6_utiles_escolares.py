"""utiles_escolares

Revision ID: b626a4f778d6
Revises: 30aa68132720
Create Date: 2026-08-15 18:41:41.700918

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = 'b626a4f778d6'
down_revision: Union[str, Sequence[str], None] = '30aa68132720'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('util_escolar',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nivel_id', sa.Integer(), nullable=False),
    sa.Column('orden', sa.Integer(), nullable=False),
    sa.Column('nombre', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('cantidad', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('asignatura', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.ForeignKeyConstraint(['nivel_id'], ['nivel.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('util_escolar')
