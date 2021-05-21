"""create-products

Revision ID: d61a4280502f
Revises: c7677c1f9d26
Create Date: 2021-05-21 13:48:49.132322

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd61a4280502f'
down_revision = 'c7677c1f9d26'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'products',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String),
        sa.Column('description', sa.String),
        sa.Column('image', sa.Integer),
        sa.Column('price', sa.String),
        sa.Column('type', sa.String),
        sa.Column('force', sa.String),                         
    )


def downgrade():
    op.drop_table('products')
