"""Chats table

Revision ID: a5b0c90b8c55
Revises: 46450316f225
Create Date: 2024-10-23 04:16:54.375321

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a5b0c90b8c55'
down_revision: Union[str, None] = '46450316f225'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chat',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('first_user_id', sa.Integer(), nullable=False),
    sa.Column('second_user_id', sa.Integer(), nullable=False),
    sa.CheckConstraint('first_user_id < second_user_id', name='_first_second_user_check'),
    sa.ForeignKeyConstraint(['first_user_id'], ['instant_chat.user.id'], ),
    sa.ForeignKeyConstraint(['second_user_id'], ['instant_chat.user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('first_user_id', 'second_user_id', name='_first_second_user_uc'),
    schema='instant_chat'
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('chat', schema='instant_chat')
    # ### end Alembic commands ###