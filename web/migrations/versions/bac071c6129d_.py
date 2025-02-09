"""empty message

Revision ID: bac071c6129d
Revises: 481042425c40
Create Date: 2020-09-01 09:51:37.051831

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'bac071c6129d'
down_revision = '481042425c40'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'hce_bids',
        sa.Column('bid_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('start_time', sa.TIMESTAMP(), nullable=False),
        sa.Column('end_time', sa.TIMESTAMP(), nullable=False),
        sa.Column('p_bid', sa.Float(), nullable=False),
        sa.Column('q_bid', sa.Float(), nullable=False),
        sa.Column('is_supply', sa.Boolean(), nullable=False),
        sa.Column('comment', sa.String(length=512), nullable=False),
        sa.Column('market_id', sa.Integer(), nullable=False),
        sa.Column('updated_at',
                  sa.TIMESTAMP(),
                  server_default=sa.text(
                      'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),
                  nullable=False),
        sa.Column('created_at',
                  sa.TIMESTAMP(),
                  server_default=sa.text('now()'),
                  nullable=True),
        sa.ForeignKeyConstraint(
            ['market_id'],
            ['markets.market_id'],
        ), sa.PrimaryKeyConstraint('bid_id'))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('hce_bids')
    # ### end Alembic commands ###
