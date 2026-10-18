"""logros_tiempo_evaluando

Revision ID: 6521290683aa
Revises: b626a4f778d6
Create Date: 2026-08-15 18:56:29.258442

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '6521290683aa'
down_revision: Union[str, Sequence[str], None] = 'b626a4f778d6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'perfil_gamificacion',
        sa.Column('tiempo_evaluando_total_seg', sa.Integer(), nullable=False, server_default='0'),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('perfil_gamificacion', 'tiempo_evaluando_total_seg')
