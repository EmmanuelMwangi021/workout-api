import sys

import pytest
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

sys.path.insert(0, "server")

from app import app  # noqa: E402
from models import db  # noqa: E402

app.config["TESTING"] = True


@pytest.fixture
def client():
    with app.app_context():
        # app.py has already initialized Flask-SQLAlchemy with the file DB.
        # Replace the app's engine before any test schema or query is run.
        db.session.remove()
        test_engine = create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        db.engines[None] = test_engine

        url = db.engine.url
        assert url.get_backend_name() == "sqlite"
        assert url.database in (None, ":memory:")
        db.create_all()

        try:
            with app.test_client() as test_client:
                yield test_client
        finally:
            db.session.remove()
            db.drop_all()
            test_engine.dispose()


def test_get_workouts(client):
    response = client.get("/workouts")
    assert response.status_code == 200
    assert response.get_json() == []


def test_create_workout(client):
    response = client.post(
        "/workouts",
        json={"date": "2026-10-24", "duration_minutes": 30, "notes": "Morning workout"},
    )
    assert response.status_code == 201
    assert response.get_json()["duration_minutes"] == 30
    assert response.get_json()["date"] == "2026-10-24"


def test_create_workout_with_invalid_data(client):
    response = client.post(
        "/workouts", json={"date": "2026-10-24", "duration_minutes": 0}
    )
    assert response.status_code == 400


def test_get_single_workout(client):
    created = client.post(
        "/workouts",
        json={"date": "2026-10-24", "duration_minutes": 45, "notes": "Leg workout"},
    )
    workout_id = created.get_json()["id"]
    response = client.get(f"/workouts/{workout_id}")
    assert response.status_code == 200
    assert response.get_json()["id"] == workout_id
    assert response.get_json()["notes"] == "Leg workout"


def test_get_missing_workout(client):
    response = client.get("/workouts/999")
    assert response.status_code == 404
    assert response.get_json()["error"] == "Workout not found"


def test_delete_workout(client):
    created = client.post(
        "/workouts", json={"date": "2026-10-24", "duration_minutes": 30}
    )
    workout_id = created.get_json()["id"]
    response = client.delete(f"/workouts/{workout_id}")
    assert response.status_code == 200
    assert response.get_json()["message"] == "Workout deleted successfully"
    assert client.get(f"/workouts/{workout_id}").status_code == 404


def test_delete_missing_workout(client):
    response = client.delete("/workouts/999")
    assert response.status_code == 404
