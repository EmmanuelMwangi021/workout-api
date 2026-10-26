from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, UniqueConstraint
from sqlalchemy.orm import validates

db= SQLAlchemy()

class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False)

    workout_exercises = db.relationship("WorkoutExercise", back_populates= "exercise")

class Workout(db.Model):
    __tablename__ = "workouts"
    __table_args__ = (
        CheckConstraint('duration_minutes > 0', name='check_workout_duration_positive'),
    )

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    workout_exercises = db.relationship("WorkoutExercise", back_populates="workout")
    
    @validates("duration_minutes")
    def validate_duration_minutes(self, key, value):
        if value<= 0:
            raise ValueError("Duration must be greater than 0")
        return value


class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"
    # The constraints allow for any value provided to be positive, optional values remain null.
    __table_args__ = (
        CheckConstraint("reps > 0 OR reps IS NULL", name= "check_reps_positive"),
        CheckConstraint("sets > 0 OR sets IS NULL", name= "check_sets_positive"),
        CheckConstraint("duration_seconds > 0 OR duration_seconds IS NULL", name= "check_duration_seconds_positive"),
        UniqueConstraint("workout_id", "exercise_id", name= "unique_exercise_per_workout"), # prevents the same exercise to be added to the same workout more than once.
    )

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"), nullable=False)
    sets = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    workout = db.relationship("Workout", back_populates="workout_exercises")
    exercise = db.relationship("Exercise", back_populates="workout_exercises")

    @validates("reps")
    def validate_reps(self, key, value):
        if value is not None and value <= 0:
            raise ValueError("Reps must be greater than 0.")
        return value

    @validates("sets")
    def validate_sets(self, key, value):
        if value is not None and value <= 0:
            raise ValueError("Sets must be greater than 0.")
        return value

    @validates("duration_seconds")
    def validate_duration_seconds(self, key, value):
        if value is not None and value <= 0:
            raise ValueError("Duration in seconds must be greater than 0.")
        return value

