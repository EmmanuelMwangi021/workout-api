from flask import Flask, request
from models import db, Exercise, Workout, WorkoutExercise
from flask_migrate import Migrate
from schemas import WorkoutSchema, ExerciseSchema, WorkoutExerciseSchema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workout.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route("/")
def home():
    return {"message": "The Workout API is running"}

#Workout Routes
# Gets all workout records
@app.route("/workouts", methods = ["GET"])
def get_workouts():
    workouts = Workout.query.all()
    schema = WorkoutSchema(many=True)
    return schema.dump(workouts), 200


#Gets a single Workout record
@app.route("/workouts/<int:id>", methods = ["GET"])
def get_workout(id):
    workout = db.session.get(Workout, id)

    if not workout:
        return{"error": "Workout not found"}, 404
    
    schema = WorkoutSchema()
    return schema.dump(workout), 200


#Creates a workout
@app.route("/workouts", methods = ["POST"])
def create_workout():
    data = request.get_json()
    try:
        workout_data = WorkoutSchema().load(data)
    except Exception as error:
        return{"error": error.messages}, 400
    
    workout = Workout(**workout_data)
    db.session.add(workout)
    db.session.commit()
    return WorkoutSchema().dump(workout), 201


#Updates a workout record
@app.route("/workouts/<int:id>", methods = ["PATCH"])
def update_workout(id):
    workout = db.session.get(Workout, id)

    if not workout:
        return {"error": "Workout not found"}, 404

    data= request.get_json()

    try:
        workout_data = WorkoutSchema(partial=True).load(data)
    except Exception as error:
        return {"error": error.messages}, 400

    for key, value in workout_data.items():
        setattr(workout, key, value)

    db.session.commit()

    return WorkoutSchema().dump(workout), 200


#Deletes a single record
@app.route("/workouts/<int:id>", methods=["DELETE"])
def delete_workout(id):
    workout = db.session.get(Workout, id)

    if not workout:
        return {"error": "Workout not found"}, 404

    db.session.delete(workout)
    db.session.commit()

    return {"message": "Workout deleted successfully"}, 200


#Exercise Routes

#Get all Exercises
@app.route("/exercises", methods = ["GET"])
def get_exercises():
    exercises = Exercise.query.all()
    schema = ExerciseSchema(many=True)

    return schema.dump(exercises), 200

#Get a single Exercise record
@app.route("/exercises/<int:id>", methods = ["GET"])
def get_exercise(id):
    exercise = db.session.get(Exercise, id)

    if not exercise:
        return{"error": "Exercise not found"}, 404
    
    schema = ExerciseSchema()
    return schema.dump(exercise), 200

#Create an Exercise
@app.route("/exercises", methods = ["POST"])
def create_exercise():
    data = request.get_json()
    try:
        exercise_data = ExerciseSchema().load(data)
    except Exception as error:
        return{"error": error.messages}, 400
    
    exercise = Exercise(**exercise_data)
    db.session.add(exercise)
    db.session.commit()
    return ExerciseSchema().dump(exercise), 201


#Deleting an Exercise record
@app.route("/exercises/<int:id>", methods=["DELETE"])
def delete_exercise(id):
    exercise = db.session.get(Exercise, id)

    if not exercise:
        return {"error": "exercise not found"}, 404

    db.session.delete(exercise)
    db.session.commit()

    return {"message": "exercise deleted successfully"}, 200


#WorkoutExercise Routes

#Gets all exercises in a workout
@app.route("/workouts/<int:workout_id>/exercises", methods = ["GET"])
def get_workout_exercises(workout_id):
    workout = db.session.get(Workout, workout_id)

    if not workout:
        return {"error": "Workout not Found"}, 404

    workout_exercises = WorkoutExercise.query.filter_by(workout_id=workout_id).all()
    
    schema = WorkoutExerciseSchema(many=True)#(serialization)
    
    return schema.dump(workout_exercises), 200


#Add an Exercise to a Workout
@app.route("/workouts/<int:workout_id>/exercises", methods = ["POST"])
def add_exercise_to_workout(workout_id):
    workout=db.session.get(Workout, workout_id)

    if not workout:
        return{"error": "Workout not found"}, 404

    data = request.get_json()

    try:
        exercise_data = WorkoutExerciseSchema().load(data)
    except Exception as error:
        return{"error": error.messages}, 400

    exercise = db.session.get(Exercise,exercise_data["exercise_id"])

    if not exercise:
        return{"error": "Exercise not Found"}, 404

    workout_exercise = WorkoutExercise(
        workout_id= workout_id,
        exercise_id = exercise_data["exercise_id"],
        reps = exercise_data.get("reps"),
        sets = exercise_data.get("sets"),
        duration_seconds = exercise_data.get("duration_seconds")
    )

    db.session.add(workout_exercise)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return{"error": "Exercise may already be added to this workout"}, 400

    return WorkoutExerciseSchema().dump(workout_exercise), 201      #Marshmallow converts the saved record into a response


if __name__ == "__main__":
    app.run(debug=True)