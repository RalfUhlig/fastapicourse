"""create users table

Revision ID: 8548f38957ae
Revises: 70c876b3d99f
Create Date: 2022-02-23 19:50:32.290333

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8548f38957ae'
down_revision = '70c876b3d99f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("users",
                    sa.Column("id", sa.Integer, nullable=False, autoincrement=True, primary_key=True),
                    sa.Column("email", sa.String(100), nullable=False, unique=True),
                    sa.Column("password", sa.String(100), nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")))


def downgrade():
    op.drop_table("users")

