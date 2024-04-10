"""Apagando a coluna 'erros' da entidade Essay V2

Revision ID: 089fcd9b0411
Revises: 95ee4d252c88
Create Date: 2024-03-31 16:14:12.116053

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '089fcd9b0411'
down_revision: Union[str, None] = '95ee4d252c88'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
