"""add relation between users and posts

Revision ID: 0d2050c9c3bb
Revises: 8548f38957ae
Create Date: 2022-02-23 20:00:44.162113

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0d2050c9c3bb'
down_revision = '8548f38957ae'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("owner_id", sa.Integer, nullable=False))
    op.create_foreign_key("fk_posts_users",
                          source_table="posts",
                          referent_table="users",
                          local_cols=["owner_id"],
                          remote_cols=["id"],
                          ondelete="CASCADE")


def downgrade():
    op.drop_constraint("fk_posts_users", table_name="posts")
    op.drop_column("posts", "owner_id")
