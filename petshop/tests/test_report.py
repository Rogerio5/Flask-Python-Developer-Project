import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_relatorio_mes_anterior(client):
    # cria uma reserva no mês anterior (agosto/2025)
    resp = client.post("/api/bookings", json={
        "date": "2025-08-15",  # mês anterior a setembro/2025
        "category_id": 1,
        "customer": {"name": "Carlos", "phone": "11977776666"},
        "pet_name": "Toby"
    })
    assert resp.status_code == 201
    booking_id = resp.get_json()["id"]

    # atualiza status para 'completed'
    resp2 = client.patch(f"/api/bookings/{booking_id}", json={"status": "completed"})
    assert resp2.status_code == 200

    # chama relatório do mês anterior
    resp3 = client.get("/api/categories/1/previous-month-bookings?month=2025-08")
    assert resp3.status_code == 200
    data = resp3.get_json()

    # validações principais
    assert data["category"]["id"] == 1
    assert data["month"] == "2025-08"
    assert data["total"] >= 1
    assert any(b["pet_name"] == "Toby" for b in data["bookings"])
