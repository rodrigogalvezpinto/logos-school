"""gamificacion_logros

Revision ID: 80fa1f62a418
Revises: d935d005f145
Create Date: 2026-08-15 16:43:34.970697

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '80fa1f62a418'
down_revision: Union[str, Sequence[str], None] = 'd935d005f145'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('perfil_gamificacion', sa.Column('racha_dias_actual', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('perfil_gamificacion', sa.Column('racha_dias_maxima', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('perfil_gamificacion', sa.Column('ultima_actividad_fecha', sa.Date(), nullable=True))
    op.add_column('perfil_gamificacion', sa.Column('guias_revisadas_total', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('perfil_gamificacion', sa.Column('evaluaciones_entregadas_total', sa.Integer(), nullable=False, server_default='0'))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('perfil_gamificacion', 'evaluaciones_entregadas_total')
    op.drop_column('perfil_gamificacion', 'guias_revisadas_total')
    op.drop_column('perfil_gamificacion', 'ultima_actividad_fecha')
    op.drop_column('perfil_gamificacion', 'racha_dias_maxima')
    op.drop_column('perfil_gamificacion', 'racha_dias_actual')
