import sys

import pytest

sys.path.insert(0, "server")

from models import Exercise, Workout, WorkoutExercise 


def test_exercise_fields_are_stored():
    exercise = Exercise(
        name="Push-ups",
        category="Strength",
        equipment_needed=False,
    )
    assert exercise.name == "Push-ups"
    assert exercise.category == "Strength"
    assert exercise.equipment_needed is False


def test_workout_duration_must_be_positive():
    with pytest.raises(ValueError):
        Workout(duration_minutes=0)


def test_workout_duration_can_be_positive():
    workout = Workout(duration_minutes=30)
    assert workout.duration_minutes == 30


def test_sets_must_be_positive():
    with pytest.raises(ValueError):
        WorkoutExercise(sets=0)


def test_duration_seconds_must_be_positive():
    with pytest.raises(ValueError):
        WorkoutExercise(duration_seconds=0)


def test_reps_can_be_positive():
    workout_exercise = WorkoutExercise(reps=10)
    assert workout_exercise.reps == 10


def test_sets_can_be_positive():
    workout_exercise = WorkoutExercise(sets=3)
    assert workout_exercise.sets == 3


def test_duration_seconds_can_be_positive():
    workout_exercise = WorkoutExercise(duration_seconds=600)
    assert workout_exercise.duration_seconds == 600
