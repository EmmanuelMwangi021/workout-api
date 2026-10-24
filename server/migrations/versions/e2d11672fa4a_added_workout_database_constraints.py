"""Added workout database constraints

Revision ID: e2d11672fa4a
Revises: 019de8d9a548
Create Date: 2026-10-24 11:07:39.705487

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2d11672fa4a'
down_revision = '019de8d9a548'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("workouts") as batch_op:
        batch_op.create_check_constraint(
            "check_workout_duration_positive",
            "duration_minutes > 0"
        )

    with op.batch_alter_table("workout_exercises") as batch_op:
        batch_op.create_check_constraint(
            "check_reps_positive",
            "reps > 0 OR reps IS NULL"
        )
        batch_op.create_check_constraint(
            "check_sets_positive",
            "sets > 0 OR sets IS NULL"
        )
        batch_op.create_check_constraint(
            "check_duration_seconds_positive",
            "duration_seconds > 0 OR duration_seconds IS NULL"
        )
        batch_op.create_unique_constraint(
            "unique_exercise_per_workout",
            ["workout_id", "exercise_id"]
        )


def downgrade():
    with op.batch_alter_table("workout_exercises") as batch_op:
        batch_op.drop_constraint(
            "unique_exercise_per_workout",
            type_="unique"
        )
        batch_op.drop_constraint(
            "check_duration_seconds_positive",
            type_="check"
        )
        batch_op.drop_constraint(
            "check_sets_positive",
            type_="check"
        )
        batch_op.drop_constraint(
            "check_reps_positive",
            type_="check"
        )

    with op.batch_alter_table("workouts") as batch_op:
        batch_op.drop_constraint(
            "check_workout_duration_positive",
            type_="check"
        )

