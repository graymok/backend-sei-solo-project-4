"""create-users

Revision ID: c7677c1f9d26
Revises: 
Create Date: 2021-05-21 13:48:43.969507

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c7677c1f9d26'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String),
        sa.Column('email', sa.String, unique=True),
        sa.Column('password', sa.String),
        sa.Column('address', sa.String),        
        sa.Column('city', sa.String),
        sa.Column('state', sa.String),
        sa.Column('zipcode', sa.String),        
        sa.Column('current', sa.Integer),
        sa.Column('lifetime', sa.Integer),        
    )


def downgrade():
    op.drop_table('users')
