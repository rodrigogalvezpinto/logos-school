"""repaso_plan_estudio

Revision ID: 32ad4dab694d
Revises: 80fa1f62a418
Create Date: 2026-08-15 16:52:45.131184

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '32ad4dab694d'
down_revision: Union[str, Sequence[str], None] = '80fa1f62a418'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('sesion_estudio', sa.Column('es_repaso', sa.Boolean(), nullable=False, server_default='false'))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('sesion_estudio', 'es_repaso')
