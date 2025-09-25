import requests

BASE_URL = "http://127.0.0.1:5000"


def print_response(action, response):
    """Imprime resposta formatada da API"""
    try:
        data = response.json()
    except Exception:
        data = response.text
    print(f"\n[{action}]")
    print("Status:", response.status_code)
    print("Resposta:", data)
    return data


# 1. Criar uma reserva
def criar_reserva():
    payload = {
        "date": "2025-09-23",
        "category_id": 1,
        "customer": {"name": "Ana Silva", "phone": "11999998888"},
        "pet_name": "Bolinha"
    }
    r = requests.post(f"{BASE_URL}/api/bookings", json=payload)
    data = print_response("Criar reserva", r)
    return data.get("id") if isinstance(data, dict) else None


# 2. Listar reservas do dia
def listar_reservas():
    r = requests.get(f"{BASE_URL}/api/bookings?date=2025-09-23")
    print_response("Listar reservas", r)


# 3. Atualizar status da reserva
def atualizar_status(booking_id):
    payload = {"status": "completed"}
    r = requests.patch(f"{BASE_URL}/api/bookings/{booking_id}", json=payload)
    print_response("Atualizar status", r)


# 4. Relatório do mês anterior
def relatorio_categoria():
    r = requests.get(f"{BASE_URL}/api/categories/1/previous-month-bookings")
    print_response("Relatório mês anterior", r)


if __name__ == "__main__":
    print("=== Testes manuais da API Petshop ===")

    booking_id = criar_reserva()
    listar_reservas()

    if booking_id:
        atualizar_status(booking_id)

    relatorio_categoria()
