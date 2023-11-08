"""Removed images from Seller

Revision ID: db67a0320467
Revises: 494bd87e621c
Create Date: 2023-11-08 08:47:03.087330

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'db67a0320467'
down_revision: Union[str, None] = '494bd87e621c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('sellers_passport_scan_key', 'sellers', type_='unique')
    op.drop_constraint('sellers_tc_scan_key', 'sellers', type_='unique')
    op.drop_column('sellers', 'passport_scan')
    op.drop_column('sellers', 'tc_scan')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sellers', sa.Column('tc_scan', sa.VARCHAR(length=130), autoincrement=False, nullable=False))
    op.add_column('sellers', sa.Column('passport_scan', sa.VARCHAR(length=130), autoincrement=False, nullable=False))
    op.create_unique_constraint('sellers_tc_scan_key', 'sellers', ['tc_scan'])
    op.create_unique_constraint('sellers_passport_scan_key', 'sellers', ['passport_scan'])
    # ### end Alembic commands ###
