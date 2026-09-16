"""sugerencias

Revision ID: 8ccac24900f8
Revises: 6521290683aa
Create Date: 2026-08-15 19:19:24.965343

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = '8ccac24900f8'
down_revision: Union[str, Sequence[str], None] = '6521290683aa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('sugerencia',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('perfil_alumno_id', sa.Integer(), nullable=False),
    sa.Column('texto', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('fecha', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['perfil_alumno_id'], ['perfilalumno.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('sugerencia')
