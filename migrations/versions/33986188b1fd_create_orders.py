"""create-orders

Revision ID: 33986188b1fd
Revises: 46b7ebc95db0
Create Date: 2021-05-21 13:49:01.321120

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '33986188b1fd'
down_revision = '46b7ebc95db0'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'orders',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer),
        sa.Column('total', sa.Integer),     
    )


def downgrade():
    op.drop_table('orders')
