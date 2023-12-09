"""Renamed Seller Model to Partner

Revision ID: 4ca0575bd6bf
Revises: 67c8e0b7b8ae
Create Date: 2023-12-09 12:12:54.118447

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '4ca0575bd6bf'
down_revision: Union[str, None] = '67c8e0b7b8ae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_users_email', table_name='users')
    op.drop_index('ix_users_id', table_name='users')
    op.drop_table('users')
    op.drop_index('ix_tokens_access_token', table_name='tokens')
    op.drop_index('ix_tokens_id', table_name='tokens')
    op.drop_table('tokens')
    op.drop_index('ix_sellers_id', table_name='sellers')
    op.drop_table('sellers')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sellers',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('mobile', sa.VARCHAR(length=30), autoincrement=False, nullable=False),
    sa.Column('company_name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('company_description', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('bank_name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('tin', sa.VARCHAR(length=12), autoincrement=False, nullable=False),
    sa.Column('bic', sa.VARCHAR(length=9), autoincrement=False, nullable=False),
    sa.Column('trrc', sa.VARCHAR(length=9), autoincrement=False, nullable=False),
    sa.Column('an', sa.VARCHAR(length=20), autoincrement=False, nullable=False),
    sa.Column('additional', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('time_created', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('is_approved', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='sellers_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='sellers_pkey'),
    sa.UniqueConstraint('an', name='sellers_an_key'),
    sa.UniqueConstraint('company_name', name='sellers_company_name_key'),
    sa.UniqueConstraint('mobile', name='sellers_mobile_key'),
    sa.UniqueConstraint('tin', name='sellers_tin_key')
    )
    op.create_index('ix_sellers_id', 'sellers', ['id'], unique=False)
    op.create_table('tokens',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('access_token', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('time_created', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='tokens_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='tokens_pkey')
    )
    op.create_index('ix_tokens_id', 'tokens', ['id'], unique=False)
    op.create_index('ix_tokens_access_token', 'tokens', ['access_token'], unique=False)
    op.create_table('users',
    sa.Column('name', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('surname', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(length=70), autoincrement=False, nullable=False),
    sa.Column('hashed_password', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('time_created', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.Column('email_confirmed', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('is_seller', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('is_admin', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('is_stuff', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('id', name='users_pkey')
    )
    op.create_index('ix_users_id', 'users', ['id'], unique=False)
    op.create_index('ix_users_email', 'users', ['email'], unique=False)
    # ### end Alembic commands ###
