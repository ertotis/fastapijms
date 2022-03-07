"""add last few columns to posts table

Revision ID: 047464f97f3c
Revises: 8cd1ce3050bf
Create Date: 2022-03-07 11:39:14.710807

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '047464f97f3c'
down_revision = '8cd1ce3050bf'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='True'),)
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)    
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')

    pass
