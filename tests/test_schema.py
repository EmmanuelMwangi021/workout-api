import sys

import pytest
from marshmallow import ValidationError

sys.path.insert(0, "server")

from schemas import ExerciseSchema, WorkoutExerciseSchema, WorkoutSchema


def test_exercise_schema_valid_data():
    data = {"name": "Push-ups", "category": "Strength", "equipment_needed": False}
    result = ExerciseSchema().load(data)
    assert result["name"] == "Push-ups"
    assert result["category"] == "Strength"
    assert result["equipment_needed"] is False


def test_exercise_schema_requires_name():
    data = {"category": "Strength", "equipment_needed": False}
    with pytest.raises(ValidationError):
        ExerciseSchema().load(data)


def test_exercise_schema_rejects_short_name():
    data = {"name": "A", "category": "Strength", "equipment_needed": False}
    with pytest.raises(ValidationError):
        ExerciseSchema().load(data)


def test_workout_schema_valid_data():
    data = {"date": "2026-10-24", "duration_minutes": 30, "notes": "Morning workout"}
    result = WorkoutSchema().load(data)
    assert result["date"].isoformat() == "2026-10-24"
    assert result["duration_minutes"] == 30


def test_workout_schema_rejects_zero_duration():
    data = {"date": "2026-10-24", "duration_minutes": 0}
    with pytest.raises(ValidationError):
        WorkoutSchema().load(data)


def test_workout_exercise_schema_rejects_zero_reps():
    data = {"exercise_id": 1, "reps": 0}
    with pytest.raises(ValidationError):
        WorkoutExerciseSchema().load(data)


def test_workout_exercise_schema_rejects_zero_sets():
    data = {"exercise_id": 1, "sets": 0}
    with pytest.raises(ValidationError):
        WorkoutExerciseSchema().load(data)


def test_workout_exercise_schema_rejects_zero_duration():
    data = {"exercise_id": 1, "duration_seconds": 0}
    with pytest.raises(ValidationError):
        WorkoutExerciseSchema().load(data)
