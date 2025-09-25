import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_reserva_categoria_inativa(client):
    # cria reserva em categoria inexistente/inativa (id=9999)
    resp = client.post("/api/bookings", json={
        "date": "2025-09-23",
        "category_id": 9999,  # categoria inválida
        "customer": {"name": "Carlos", "phone": "11977776666"},
        "pet_name": "Toby"
    })
    assert resp.status_code == 400
    data = resp.get_json()
    assert data["error"] == "invalid_category"


def test_atualizar_status_invalido(client):
    # cria reserva válida
    resp = client.post("/api/bookings", json={
        "date": "2025-09-23",
        "category_id": 1,
        "customer": {"name": "Ana", "phone": "11988887777"},
        "pet_name": "Rex"
    })
    booking_id = resp.get_json()["id"]

    # tenta atualizar com status inválido
    resp2 = client.patch(f"/api/bookings/{booking_id}", json={"status": "done"})
    assert resp2.status_code == 400
    data = resp2.get_json()
    assert data["error"] == "invalid_status"


def test_atualizar_reserva_inexistente(client):
    # tenta atualizar reserva que não existe
    resp = client.patch("/api/bookings/99999", json={"status": "completed"})
    assert resp.status_code == 404
    data = resp.get_json()
    assert data["error"] == "not_found"
