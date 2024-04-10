"""Alterando o tipo das colunas de nota para inteiro

Revision ID: 9a0b373ae799
Revises: 578b84668289
Create Date: 2024-03-31 16:20:02.149326

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9a0b373ae799"
down_revision: Union[str, None] = "578b84668289"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "essay",
        "criteria_score_5",
        existing_type=sa.Float(),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
    op.alter_column(
        "essay",
        "criteria_score_4",
        existing_type=sa.Float(),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
    op.alter_column(
        "essay",
        "criteria_score_3",
        existing_type=sa.Float(),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
    op.alter_column(
        "essay",
        "criteria_score_2",
        existing_type=sa.Float(),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
    op.alter_column(
        "essay",
        "criteria_score_1",
        existing_type=sa.Float(),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
    op.alter_column(
        "essay",
        "final_score",
        existing_type=sa.Float(),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    pass