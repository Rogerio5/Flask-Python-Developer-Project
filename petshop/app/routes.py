from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime, date, timedelta
from .models import db, Reserva, Categoria, Cliente

bp = Blueprint("main", __name__)

# ---------------------------
# Rotas de Páginas HTML
# ---------------------------

@bp.route("/")
def home():
    """Página inicial com formulário de agendamento"""
    categorias = Categoria.query.filter_by(ativo=True).all()
    return render_template("agendar.html", categorias=categorias)

@bp.route("/reservas")
@login_required
def reservas():
    """Página para listar reservas"""
    if current_user.is_admin:
        reservas = Reserva.query.order_by(Reserva.data.asc()).all()
    else:
        reservas = Reserva.query.join(Cliente).filter(Cliente.id == current_user.id).all()
    return render_template("reservas.html", reservas=reservas)

@bp.route("/reserva/<int:reserva_id>")
@login_required
def reserva_detail(reserva_id):
    """Detalhes de uma reserva"""
    reserva = Reserva.query.get_or_404(reserva_id)
    return render_template("reserva_detail.html", reserva=reserva)

@bp.route("/reserva/<int:reserva_id>/editar", methods=["GET", "POST"])
@login_required
def reserva_edit(reserva_id):
    """Editar uma reserva"""
    reserva = Reserva.query.get_or_404(reserva_id)
    if request.method == "POST":
        reserva.pet_nome = request.form["pet_nome"]
        reserva.data = datetime.strptime(request.form["data"], "%Y-%m-%d").date()
        reserva.status = request.form.get("status", reserva.status)
        db.session.commit()
        flash("Reserva atualizada com sucesso!", "success")
        return redirect(url_for("main.reserva_detail", reserva_id=reserva.id))
    return render_template("reserva_edit.html", reserva=reserva)

@bp.route("/reserva/<int:reserva_id>/cancelar")
@login_required
def reserva_cancel(reserva_id):
    """Cancelar uma reserva"""
    reserva = Reserva.query.get_or_404(reserva_id)
    reserva.status = "cancelado"
    db.session.commit()
    flash("Reserva cancelada com sucesso!", "warning")
    return redirect(url_for("main.reservas"))

@bp.route("/relatorios")
@login_required
def relatorios():
    """Relatórios de reservas"""
    hoje = date.today()
    semana_inicio = hoje - timedelta(days=hoje.weekday())
    semana_fim = semana_inicio + timedelta(days=6)

    total_semana = Reserva.query.filter(Reserva.data.between(semana_inicio, semana_fim)).count()
    total_mes = Reserva.query.filter(
        Reserva.data.between(hoje.replace(day=1), hoje)
    ).count()

    categorias = db.session.query(Categoria.nome, db.func.count(Reserva.id)).join(Reserva).group_by(Categoria.nome).all()

    return render_template("relatorios.html", total_semana=total_semana, total_mes=total_mes, categorias=categorias)

# ---------------------------
# Rotas da API
# ---------------------------

@bp.route("/api/reservas", methods=["POST"])
def criar_reserva():
    """Criar nova reserva via API"""
    dados = request.get_json() or {}
    try:
        data = datetime.strptime(dados["data"], "%Y-%m-%d").date()
        categoria_id = int(dados["categoria_id"])
        nome_dono = dados["nome_dono"].strip()
        telefone = dados["telefone"].strip()
        pet_nome = dados["nome_pet"].strip()
    except (KeyError, ValueError, AttributeError):
        return jsonify({"error": "invalid_payload", "message": "Campos obrigatórios ausentes ou inválidos."}), 400

    categoria = Categoria.query.get(categoria_id)
    if not categoria or not categoria.ativo:
        return jsonify({"error": "invalid_category", "message": "Categoria inválida ou inativa."}), 400

    total = Reserva.query.filter_by(data=data).count()
    if total >= 10:
        return jsonify({
            "error": "capacity_exceeded",
            "message": f"Capacidade máxima de 10 agendamentos atingida para {data}."
        }), 409

    cliente = Cliente.query.filter_by(nome=nome_dono, telefone=telefone).first()
    if not cliente:
        cliente = Cliente(nome=nome_dono, telefone=telefone)
        db.session.add(cliente)
        db.session.flush()

    reserva = Reserva(
        pet_nome=pet_nome,
        data=data,
        categoria_id=categoria_id,
        cliente_id=cliente.id
    )
    db.session.add(reserva)
    db.session.commit()

    return jsonify(reserva.to_dict()), 201

@bp.route("/api/reservas/<int:reserva_id>", methods=["PATCH"])
def atualizar_reserva(reserva_id):
    """Atualizar status da reserva"""
    dados = request.get_json() or {}
    status = dados.get("status")

    if status not in ("agendado", "concluido", "cancelado"):
        return jsonify({"error": "invalid_status", "message": "Status inválido."}), 400

    reserva = Reserva.query.get(reserva_id)
    if not reserva:
        return jsonify({"error": "not_found", "message": "Reserva não encontrada."}), 404

    reserva.status = status
    db.session.commit()
    return jsonify(reserva.to_dict()), 200


# ---------------------------
# Rotas auxiliares (opcional)
# ---------------------------

@bp.route("/api/reservas/<int:reserva_id>", methods=["GET"])
def obter_reserva(reserva_id):
    """Obter detalhes de uma reserva específica"""
    reserva = Reserva.query.get(reserva_id)
    if not reserva:
        return jsonify({"error": "not_found", "message": "Reserva não encontrada."}), 404
    return jsonify(reserva.to_dict()), 200


@bp.route("/api/reservas/<int:reserva_id>", methods=["DELETE"])
def deletar_reserva(reserva_id):
    """Cancelar (deletar) uma reserva"""
    reserva = Reserva.query.get(reserva_id)
    if not reserva:
        return jsonify({"error": "not_found", "message": "Reserva não encontrada."}), 404

    db.session.delete(reserva)
    db.session.commit()
    return jsonify({"message": "Reserva cancelada com sucesso."}), 200

