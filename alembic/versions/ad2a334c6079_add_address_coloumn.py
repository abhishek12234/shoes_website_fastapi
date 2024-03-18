"""add_address_coloumn

Revision ID: ad2a334c6079
Revises: 88813de53009
Create Date: 2024-03-18 22:23:38.423646

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ad2a334c6079'
down_revision: Union[str, None] = '88813de53009'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('user_address', sa.String(), server_default='none'))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'user_address')
    # ### end Alembic commands ###
