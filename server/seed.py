from datetime import date
from app import app
from models import db, Exercise, Workout, WorkoutExercise

with app.app_context():
    #clears existing data 
    Exercise.query.delete()
    Workout.query.delete()
    WorkoutExercise.query.delete()
    
    # Creating an Exercise
    push_ups = Exercise(
        name = "Push-ups",
        category = "Strength",
        equipment_needed = False
    )

    squats = Exercise(
       name = "Squats",
       category = "Strength",
       equipment_needed = False 
    )

    running = Exercise(
        name = "Running",
        category = "Cardio",
        equipment_needed = True
    )

    bench_press = Exercise(
        name = "Barbell_Bench_Press",
        category = "Strength",
        equipment_needed = True
    )

    db.session.add_all([push_ups, squats, running, bench_press])
    db.session.flush()       #assigns id before we create related records

    #Creating a workout
    workout1 = Workout(
        date = date.today(),
        duration_minutes = 40,
        notes = "Full body workout"
    )

    db.session.add(workout1)
    db.session.flush()

    #Connecting exercises to workouts
    workout_push_ups = WorkoutExercise(
        workout_id = workout1.id,
        exercise_id = push_ups.id,
        reps = 12,
        sets = 3
    )

    workout_squats = WorkoutExercise(
        workout_id = workout1.id,
        exercise_id = squats.id,
        reps = 15,
        sets = 3
    )

    workout_running = WorkoutExercise(
        workout_id = workout1.id,
        exercise_id = running.id,
        duration_seconds = 600
    )

    workout_bench_press = WorkoutExercise(
        workout_id = workout1.id,
        exercise_id = bench_press.id,
        reps = 10,
        sets = 3
    )

    db.session.add_all([workout_push_ups, workout_squats, workout_running, workout_bench_press])
    db.session.commit()
    #print("Seed data added successfully!")
