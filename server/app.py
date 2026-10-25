from flask import Flask, request
from models import db, Exercise, Workout, WorkoutExercise
from flask_migrate import Migrate
from schemas import WorkoutSchema, ExerciseSchema

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




if __name__ == "__main__":
    app.run(debug=True)