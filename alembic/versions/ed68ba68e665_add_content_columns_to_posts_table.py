"""add content columns to posts table

Revision ID: ed68ba68e665
Revises: 1d2623b5b29c
Create Date: 2022-02-28 12:11:52.661865

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ed68ba68e665'
down_revision = '1d2623b5b29c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
