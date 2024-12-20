"""user

Revision ID: c551cc5b5732
Revises: c399117fb4df
Create Date: 2024-11-21 23:28:56.577803

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c551cc5b5732'
down_revision: Union[str, None] = 'c399117fb4df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('updated_at', postgresql.TIMESTAMP(), nullable=True))
    op.drop_column('users', 'update_at')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('update_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_column('users', 'updated_at')
    # ### end Alembic commands ###
