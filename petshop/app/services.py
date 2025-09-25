from .models import db, Reserva, Categoria, Cliente, CapacidadeDiaria
from datetime import date, timedelta
from sqlalchemy import func

# Capacidade padrão por dia (se não houver registro em CapacidadeDiaria)
DEFAULT_CAPACITY = 10


# ============================
# Funções de capacidade
# ============================

def capacity_for_day(dia: date) -> int:
    """
    Retorna a capacidade máxima de agendamentos para um dia.
    Se não houver configuração específica em CapacidadeDiaria,
    usa o valor padrão.
    """
    capacidade = CapacidadeDiaria.query.filter_by(data=dia).first()
    return capacidade.max_reservas if capacidade else DEFAULT_CAPACITY


def bookings_count(dia: date) -> int:
    """
    Conta quantas reservas já existem em um dia (status agendado ou concluído).
    """
    return Reserva.query.filter(
        Reserva.data == dia,
        Reserva.status.in_(["agendado", "concluido"])
    ).count()


def pode_agendar(dia: date) -> bool:
    """
    Verifica se ainda há vagas disponíveis para o dia.
    """
    return bookings_count(dia) < capacity_for_day(dia)


# ============================
# Funções de reservas
# ============================

def criar_reserva(nome_dono: str, telefone: str, nome_pet: str, categoria_id: int, dia: date) -> Reserva:
    """
    Cria uma nova reserva no banco, vinculando cliente e categoria.
    """
    if not pode_agendar(dia):
        raise ValueError(f"Limite de agendamentos atingido para {dia}")

    # Verifica se a categoria existe e está ativa
    categoria = Categoria.query.get(categoria_id)
    if not categoria or not categoria.ativo:
        raise ValueError("Categoria inválida ou inativa")

    # Busca cliente existente ou cria novo
    cliente = Cliente.query.filter_by(nome=nome_dono, telefone=telefone).first()
    if not cliente:
        cliente = Cliente(nome=nome_dono, telefone=telefone)
        db.session.add(cliente)
        db.session.flush()  # garante ID antes de criar reserva

    # Cria reserva
    reserva = Reserva(
        pet_nome=nome_pet,
        data=dia,
        categoria_id=categoria_id,
        cliente_id=cliente.id,
        status="agendado"
    )
    db.session.add(reserva)
    db.session.commit()
    return reserva


def atualizar_status(reserva_id: int, status: str) -> Reserva:
    """
    Atualiza o status de uma reserva.
    Status válidos: agendado, concluido, cancelado.
    """
    if status not in Reserva.STATUS_CHOICES:
        raise ValueError("Status inválido")

    reserva = Reserva.query.get(reserva_id)
    if not reserva:
        raise LookupError("Reserva não encontrada")

    reserva.status = status
    db.session.commit()
    return reserva


def cancelar_reserva(reserva_id: int) -> None:
    """
    Cancela (deleta) uma reserva do banco.
    """
    reserva = Reserva.query.get(reserva_id)
    if not reserva:
        raise LookupError("Reserva não encontrada")

    db.session.delete(reserva)
    db.session.commit()


# ============================
# Funções de relatórios
# ============================

def total_reservas_semana(hoje: date) -> int:
    """
    Retorna o total de reservas na semana atual.
    """
    semana_inicio = hoje - timedelta(days=hoje.weekday())
    semana_fim = semana_inicio + timedelta(days=6)
    return Reserva.query.filter(Reserva.data.between(semana_inicio, semana_fim)).count()


def total_reservas_mes(hoje: date) -> int:
    """
    Retorna o total de reservas no mês atual.
    """
    primeiro_dia_mes = hoje.replace(day=1)
    return Reserva.query.filter(Reserva.data.between(primeiro_dia_mes, hoje)).count()


def categorias_mais_comuns() -> list:
    """
    Retorna uma lista de tuplas (categoria, quantidade) ordenada por quantidade.
    """
    return db.session.query(
        Categoria.nome,
        func.count(Reserva.id)
    ).join(Reserva).group_by(Categoria.nome).order_by(func.count(Reserva.id).desc()).all()
