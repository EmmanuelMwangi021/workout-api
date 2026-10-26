"""Corrected workout and exercise field types and added model validators

Revision ID: 59ab7f468159
Revises: e2d11672fa4a
Create Date: 2026-10-26 08:24:51.496868

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '59ab7f468159'
down_revision = 'e2d11672fa4a'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("exercises", recreate="always") as batch_op:
        batch_op.alter_column(
            "equipment_needed",
            existing_type=sa.VARCHAR(),
            type_=sa.Boolean(),
            existing_nullable=False,
        )

    with op.batch_alter_table("workouts", recreate="always") as batch_op:
        batch_op.alter_column(
            "date",
            existing_type=sa.DATETIME(),
            type_=sa.Date(),
            existing_nullable=False,
        )


def downgrade():
    with op.batch_alter_table("workouts", recreate="always") as batch_op:
        batch_op.alter_column(
            "date",
            existing_type=sa.Date(),
            type_=sa.DateTime(),
            existing_nullable=False,
        )

    with op.batch_alter_table("exercises", recreate="always") as batch_op:
        batch_op.alter_column(
            "equipment_needed",
            existing_type=sa.Boolean(),
            type_=sa.VARCHAR(),
            existing_nullable=False,
        )