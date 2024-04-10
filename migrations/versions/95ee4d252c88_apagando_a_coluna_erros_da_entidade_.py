"""Apagando a coluna 'erros' da entidade Essay

Revision ID: 95ee4d252c88
Revises: 93d42aee0c8b
Create Date: 2024-03-31 16:13:23.883253

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '95ee4d252c88'
down_revision: Union[str, None] = '93d42aee0c8b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
