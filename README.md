# Workout API

A Flask REST API for recording workouts, exercises, and the exercises performed in each workout. Data is stored in SQLite and managed with Flask-Migrate.

## Requirements

- Python 3
- pip

## Setup

From the project root, create and activate a virtual environment, then install the dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Create or update the database

The migration scripts are in `server/migrations/`. Run the migration command from the `server/` directory:

```bash
cd server
flask --app app db upgrade
```

## Run the API

From the `server/` directory, start the development server:

```bash
flask --app app run --debug
```

The API is available at `http://127.0.0.1:5000`. The home route, `/`, returns a message confirming that the API is running.

## Seed sample data

From `server/`, run:

```bash
python seed.py
```

**Warning:** The seed script deletes existing exercises, workouts, and workout-exercise records before inserting its sample data. Running it again replaces those records.

## API routes

| Method | Route | Description |
| --- | --- | --- |
| GET | `/` | API status |
| GET | `/workouts` | List workouts |
| POST | `/workouts` | Create a workout |
| GET | `/workouts/<id>` | Get one workout |
| PATCH | `/workouts/<id>` | Update workout fields |
| DELETE | `/workouts/<id>` | Delete a workout |
| GET | `/exercises` | List exercises |
| POST | `/exercises` | Create an exercise |
| GET | `/exercises/<id>` | Get one exercise |
| DELETE | `/exercises/<id>` | Delete an exercise |
| GET | `/workouts/<workout_id>/exercises` | List exercises in a workout |
| POST | `/workouts/<workout_id>/exercises` | Add an exercise to a workout |

### Example requests

Create a workout:

```bash
curl -X POST http://127.0.0.1:5000/workouts \\
  -H "Content-Type: application/json" \\
  -d '{"date":("Your date"),"duration_minutes":(Your minutes),"notes":"Full body workout"}'
```

Create an exercise:

```bash
curl -X POST http://127.0.0.1:5000/exercises \\
  -H "Content-Type: application/json" \\
  -d '{"name":("Your Exercise"),"category":"Strength","equipment_needed":false}'
```

Add an exercise to a workout (replace the IDs with existing records):

```bash
curl -X POST http://127.0.0.1:5000/workouts/1/exercises \\
  -H "Content-Type: application/json" \\
  -d '{"exercise_id":1,"reps":12,"sets":3}'
```
Remember to replace the values in brackets with real values. The API will give respective errors.

## Tests

Run the test suite from the project root with the virtual environment active:

```bash
pytest
```

The API tests use an in-memory SQLite database and do not use the app's SQLite database file.

