"""Add user table

Revision ID: 076826363235
Revises: ed68ba68e665
Create Date: 2022-03-07 11:27:33.063936

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '076826363235'
down_revision = 'ed68ba68e665'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                sa.Column('id', sa.Integer(), nullable=False),
                sa.Column('email', sa.String(), nullable=False),
                sa.Column('password', sa.String(), nullable=False),
                sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                            server_default=sa.text('now()'),nullable=False),
                sa.PrimaryKeyConstraint('id'),
                sa.UniqueConstraint('email')
                )   
    pass


def downgrade():
    op.drop_table('users')
    pass
