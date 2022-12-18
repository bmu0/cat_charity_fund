"""diff datetimes

Revision ID: 9ccf2543e2c8
Revises: 6e59a50951ae
Create Date: 2022-12-16 16:45:15.766605

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9ccf2543e2c8'
down_revision = '6e59a50951ae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('create_date', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('close_date', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('close_date')
        batch_op.drop_column('create_date')

    # ### end Alembic commands ###
