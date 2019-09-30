"""empty message

Revision ID: 8199e2c69f84
Revises: 
Create Date: 2019-09-30 23:48:58.350065

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8199e2c69f84'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('journal',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('creation_date', sa.TIMESTAMP(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('content', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('journal')
    # ### end Alembic commands ###