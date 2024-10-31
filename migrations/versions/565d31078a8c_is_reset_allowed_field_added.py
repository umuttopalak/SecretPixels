"""is_reset_allowed field added

Revision ID: 565d31078a8c
Revises: 35237ce0fbcd
Create Date: 2024-11-01 01:45:08.671681

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '565d31078a8c'
down_revision: Union[str, None] = '35237ce0fbcd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('forgot_password_token', sa.Column('is_reset_allowed', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('forgot_password_token', 'is_reset_allowed')
    # ### end Alembic commands ###
