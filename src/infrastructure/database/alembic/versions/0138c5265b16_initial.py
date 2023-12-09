"""initial

Revision ID: 0138c5265b16
Revises: 
Create Date: 2023-11-08 12:13:33.946574

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '0138c5265b16'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('surname', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=70), nullable=False),
    sa.Column('hashed_password', sa.String(length=100), nullable=False),
    sa.Column('time_created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('email_confirmed', sa.Boolean(), nullable=False),
    sa.Column('is_seller', sa.Boolean(), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=False),
    sa.Column('is_stuff', sa.Boolean(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_table('sellers',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('mobile', sa.String(length=30), nullable=False),
    sa.Column('company_name', sa.String(), nullable=False),
    sa.Column('company_description', sa.Text(), nullable=False),
    sa.Column('bank_name', sa.String(), nullable=False),
    sa.Column('tin', sa.String(length=12), nullable=False),
    sa.Column('bic', sa.String(length=9), nullable=False),
    sa.Column('trrc', sa.String(length=9), nullable=False),
    sa.Column('an', sa.String(length=20), nullable=False),
    sa.Column('additional', sa.Text(), nullable=True),
    sa.Column('time_created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('is_approved', sa.Boolean(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('an'),
    sa.UniqueConstraint('company_name'),
    sa.UniqueConstraint('mobile'),
    sa.UniqueConstraint('tin')
    )
    op.create_index(op.f('ix_sellers_id'), 'sellers', ['id'], unique=False)
    op.create_table('tokens',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('access_token', sa.String(), nullable=False),
    sa.Column('time_created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tokens_access_token'), 'tokens', ['access_token'], unique=True)
    op.create_index(op.f('ix_tokens_id'), 'tokens', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_tokens_id'), table_name='tokens')
    op.drop_index(op.f('ix_tokens_access_token'), table_name='tokens')
    op.drop_table('tokens')
    op.drop_index(op.f('ix_sellers_id'), table_name='sellers')
    op.drop_table('sellers')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###