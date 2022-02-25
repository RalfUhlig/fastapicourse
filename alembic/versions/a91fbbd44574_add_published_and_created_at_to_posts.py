"""add published and created_at to posts

Revision ID: a91fbbd44574
Revises: 0d2050c9c3bb
Create Date: 2022-02-23 20:11:10.940282

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a91fbbd44574'
down_revision = '0d2050c9c3bb'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("published", sa.Boolean, nullable=False, server_default="1"))
    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")))


def downgrade():
    op.drop_column("posts, created_at")
    op.drop_column("posts, published")
