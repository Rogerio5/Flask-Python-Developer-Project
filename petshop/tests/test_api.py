import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_criar_reserva(client):
    resp = client.post("/api/bookings", json={
        "date": "2025-09-23",
        "category_id": 1,
        "customer": {"name": "Teste", "phone": "11999999999"},
        "pet_name": "Rex"
    })
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["status"] == "scheduled"

def test_listar_reservas(client):
    resp = client.get("/api/bookings?date=2025-09-23")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)

def test_atualizar_status(client):
    # cria reserva primeiro
    resp = client.post("/api/bookings", json={
        "date": "2025-09-24",
        "category_id": 1,
        "customer": {"name": "Maria", "phone": "11988887777"},
        "pet_name": "Luna"
    })
    booking_id = resp.get_json()["id"]

    # atualiza status
    resp2 = client.patch(f"/api/bookings/{booking_id}", json={"status": "completed"})
    assert resp2.status_code == 200
    assert resp2.get_json()["status"] == "completed"
