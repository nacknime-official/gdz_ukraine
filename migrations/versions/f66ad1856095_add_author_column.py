"""add author column

Revision ID: f66ad1856095
Revises: 746a1d372012
Create Date: 2020-05-11 11:45:02.743064

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f66ad1856095'
down_revision = '746a1d372012'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('author', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'author')
    # ### end Alembic commands ###
