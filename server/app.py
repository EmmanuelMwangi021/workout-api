from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db, Exercise, Workout, WorkoutExercise
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workout.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route("/")
def home():
    return {"message": "The Workout API is running"}






if __name__ == "__main__":
    app.run(debug=True)