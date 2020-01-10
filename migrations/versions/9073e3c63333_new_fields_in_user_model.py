"""new fields in user model

Revision ID: 9073e3c63333
Revises: eedd67461fc4
Create Date: 2020-01-09 11:56:59.887306

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9073e3c63333'
down_revision = 'eedd67461fc4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('first_name', sa.String(length=50), nullable=True))
    op.add_column('user', sa.Column('last_name', sa.String(length=50), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'last_name')
    op.drop_column('user', 'first_name')
    # ### end Alembic commands ###
