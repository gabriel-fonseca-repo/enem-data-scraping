"""Mudando tipo da coluna prompt de String para Text

Revision ID: 8e676dadc3c5
Revises: 2386b1c5b271
Create Date: 2024-03-28 12:57:20.571662

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8e676dadc3c5'
down_revision: Union[str, None] = '2386b1c5b271'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('essay', 'prompt',
               existing_type=sa.VARCHAR(),
               type_=sa.Text(),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('essay', 'prompt',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(),
               existing_nullable=False)
    # ### end Alembic commands ###