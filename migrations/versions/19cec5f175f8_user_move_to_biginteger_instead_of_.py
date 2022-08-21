"""user: move to BigInteger instead of Integer

Revision ID: 19cec5f175f8
Revises: e867d8d5dcde
Create Date: 2022-08-21 22:13:14.825606

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '19cec5f175f8'
down_revision = 'e867d8d5dcde'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('users', 'user_id',
               existing_type=sa.INTEGER(),
               type_=sa.BigInteger(),
               existing_nullable=False,
               autoincrement=True,
               existing_server_default=sa.text("nextval('users_id_seq'::regclass)"))


def downgrade():
    op.alter_column('users', 'user_id',
               existing_type=sa.BigInteger(),
               type_=sa.INTEGER(),
               existing_nullable=False,
               autoincrement=True,
               existing_server_default=sa.text("nextval('users_id_seq'::regclass)"))

