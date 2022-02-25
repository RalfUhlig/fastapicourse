"""Create posts table

Revision ID: 70c876b3d99f
Revises: 
Create Date: 2022-02-23 16:34:49.105273

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '70c876b3d99f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("posts",
                    sa.Column("id", sa.Integer, nullable=False, autoincrement=True, primary_key=True),
                    sa.Column("title", sa.String(100), nullable=False),
                    sa.Column("content", sa.String(1000), nullable=False))


def downgrade():
    op.drop_table("posts")
