"""refactor: rename user.class to user.grade

Revision ID: efa23160c50b
Revises: 939b77481d94
Create Date: 2020-06-03 11:43:55.982140

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "efa23160c50b"
down_revision = "939b77481d94"
branch_labels = None
depends_on = None


def upgrade():
    # changed manually
    op.alter_column("users", "class_", new_column_name="grade")


def downgrade():
    # changed manually
    op.alter_column("users", "grade", new_column_name="class_")
