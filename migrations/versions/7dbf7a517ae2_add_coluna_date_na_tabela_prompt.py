"""Add coluna date na tabela prompt

Revision ID: 7dbf7a517ae2
Revises: f6dd4b7b7c4d
Create Date: 2024-03-28 18:46:40.497070

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7dbf7a517ae2'
down_revision: Union[str, None] = 'f6dd4b7b7c4d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('prompt', sa.Column('date', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('prompt', 'date')
    # ### end Alembic commands ###