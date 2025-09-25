import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_limite_de_capacidade(client):
    dia = "2025-09-25"

    # Cria 10 reservas válidas
    for i in range(10):
        resp = client.post("/api/bookings", json={
            "date": dia,
            "category_id": 1,
            "customer": {"name": f"Cliente {i}", "phone": f"119999900{i:02d}"},
            "pet_name": f"Pet {i}"
        })
        assert resp.status_code == 201  # todas devem ser criadas com sucesso

    # Tenta criar a 11ª reserva → deve falhar
    resp = client.post("/api/bookings", json={
        "date": dia,
        "category_id": 1,
        "customer": {"name": "Cliente 11", "phone": "11999991111"},
        "pet_name": "Pet 11"
    })

    assert resp.status_code == 409  # conflito de capacidade
    data = resp.get_json()
    assert data["error"] == "capacity_exceeded"
    assert "Capacidade máxima" in data["message"]
