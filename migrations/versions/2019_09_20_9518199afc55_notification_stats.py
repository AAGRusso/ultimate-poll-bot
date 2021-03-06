"""Notification stats

Revision ID: 9518199afc55
Revises: c8c17d4869a8
Create Date: 2019-09-20 14:48:53.985100

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "9518199afc55"
down_revision = "c8c17d4869a8"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "daily_statistic",
        sa.Column("notifications", sa.Integer(), server_default="0", nullable=False),
    )
    op.alter_column(
        "daily_statistic",
        "externally_shared",
        existing_type=sa.INTEGER(),
        server_default=None,
        existing_nullable=False,
    )
    op.alter_column(
        "daily_statistic",
        "show_results",
        existing_type=sa.INTEGER(),
        server_default=None,
        existing_nullable=False,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "daily_statistic",
        "show_results",
        existing_type=sa.INTEGER(),
        server_default=sa.text("0"),
        existing_nullable=False,
    )
    op.alter_column(
        "daily_statistic",
        "externally_shared",
        existing_type=sa.INTEGER(),
        server_default=sa.text("0"),
        existing_nullable=False,
    )
    op.drop_column("daily_statistic", "notifications")
    # ### end Alembic commands ###
