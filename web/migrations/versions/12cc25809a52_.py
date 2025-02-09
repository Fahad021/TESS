"""empty message

Revision ID: 12cc25809a52
Revises: 4e02dc1f15c7
Create Date: 2020-09-14 20:59:31.595568

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '12cc25809a52'
down_revision = '4e02dc1f15c7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'eventing_devices',
        sa.Column('ed_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('device_id', sa.String(length=64), nullable=True),
        sa.PrimaryKeyConstraint('ed_id'), sa.UniqueConstraint('device_id'))
    op.add_column('device_events',
                  sa.Column('ed_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'device_events', 'eventing_devices', ['ed_id'],
                          ['ed_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'device_events', type_='foreignkey')
    op.drop_column('device_events', 'ed_id')
    op.drop_table('eventing_devices')
    # ### end Alembic commands ###
