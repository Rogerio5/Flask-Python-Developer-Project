import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_reserva_sem_nome(client):
    resp = client.post("/api/bookings", json={
        "date": "2025-09-23",
        "category_id": 1,
        "customer": {"phone": "11999999999"},  # faltando nome
        "pet_name": "Rex"
    })
    assert resp.status_code == 400
    data = resp.get_json()
    assert data["error"] == "invalid_payload"


def test_reserva_sem_telefone(client):
    resp = client.post("/api/bookings", json={
        "date": "2025-09-23",
        "category_id": 1,
        "customer": {"name": "Maria"},  # faltando telefone
        "pet_name": "Luna"
    })
    assert resp.status_code == 400
    data = resp.get_json()
    assert data["error"] == "invalid_payload"


def test_reserva_sem_categoria(client):
    resp = client.post("/api/bookings", json={
        "date": "2025-09-23",
        "customer": {"name": "João", "phone": "11988887777"},
        "pet_name": "Bidu"
    })
    assert resp.status_code == 400
    data = resp.get_json()
    assert data["error"] == "invalid_payload"


def test_reserva_sem_data(client):
    resp = client.post("/api/bookings", json={
        "category_id": 1,
        "customer": {"name": "Ana", "phone": "11977776666"},
        "pet_name": "Mel"
    })
    assert resp.status_code == 400
    data = resp.get_json()
    assert data["error"] == "invalid_payload"
