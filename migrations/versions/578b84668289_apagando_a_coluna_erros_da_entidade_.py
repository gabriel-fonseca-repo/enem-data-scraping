"""Apagando a coluna 'erros' da entidade Essay V4

Revision ID: 578b84668289
Revises: d4ba71650d59
Create Date: 2024-03-31 16:16:58.332868

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "578b84668289"
down_revision: Union[str, None] = "d4ba71650d59"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("essay", "errors")


def downgrade() -> None:
    pass
