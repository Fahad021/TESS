"""empty message

Revision ID: 4e02dc1f15c7
Revises: bac071c6129d
Create Date: 2020-09-09 20:21:07.876012

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '4e02dc1f15c7'
down_revision = 'bac071c6129d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'device_events',
        sa.Column('des_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('event_data', sa.JSON(), nullable=True),
        sa.Column('created_at',
                  sa.TIMESTAMP(),
                  server_default=sa.text('now()'),
                  nullable=True), sa.PrimaryKeyConstraint('des_id'))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('device_events')
    # ### end Alembic commands ###
