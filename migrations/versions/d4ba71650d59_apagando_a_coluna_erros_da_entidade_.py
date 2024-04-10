"""Apagando a coluna 'erros' da entidade Essay V3

Revision ID: d4ba71650d59
Revises: 089fcd9b0411
Create Date: 2024-03-31 16:16:26.346016

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd4ba71650d59'
down_revision: Union[str, None] = '089fcd9b0411'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
