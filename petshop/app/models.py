from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# ============================
# Usuário do sistema (admin, gerente, etc.)
# ============================
class Usuario(UserMixin, db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    senha_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    def set_password(self, senha: str):
        """Define a senha do usuário (armazenada como hash)."""
        self.senha_hash = generate_password_hash(senha)

    def check_password(self, senha: str) -> bool:
        """Verifica se a senha informada confere com o hash armazenado."""
        return check_password_hash(self.senha_hash, senha)

    def __repr__(self):
        return f"<Usuario {self.username}>"


# ============================
# Categorias de animais (Cachorro, Gato, Coelho etc.)
# ============================
class Categoria(db.Model):
    __tablename__ = "categorias_animais"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), unique=True, nullable=False)
    ativo = db.Column(db.Boolean, default=True, nullable=False)

    reservas = db.relationship("Reserva", back_populates="categoria", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Categoria {self.nome}>"


# ============================
# Capacidade diária (limite de reservas por dia)
# ============================
class CapacidadeDiaria(db.Model):
    __tablename__ = "capacidade_diaria"

    data = db.Column(db.Date, primary_key=True)
    max_reservas = db.Column(db.Integer, nullable=False, default=10)

    def __repr__(self):
        return f"<Capacidade {self.data} - {self.max_reservas}>"


# ============================
# Clientes
# ============================
class Cliente(db.Model):
    __tablename__ = "clientes"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)

    reservas = db.relationship("Reserva", back_populates="cliente", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Cliente {self.nome}>"


# ============================
# Reservas de banho
# ============================
class Reserva(db.Model):
    __tablename__ = "reservas"

    STATUS_CHOICES = ("agendado", "concluido", "cancelado")

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, nullable=False)
    pet_nome = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default="agendado", nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    categoria_id = db.Column(db.Integer, db.ForeignKey("categorias_animais.id"), nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id"), nullable=False)

    categoria = db.relationship("Categoria", back_populates="reservas")
    cliente = db.relationship("Cliente", back_populates="reservas")

    def to_dict(self):
        return {
            "id": self.id,
            "data": self.data.isoformat(),
            "pet_nome": self.pet_nome,
            "status": self.status,
            "criado_em": self.criado_em.isoformat(),
            "cliente": {
                "id": self.cliente.id,
                "nome": self.cliente.nome,
                "telefone": self.cliente.telefone
            } if self.cliente else None,
            "categoria": self.categoria.nome if self.categoria else None
        }

    def __repr__(self):
        return f"<Reserva {self.pet_nome} em {self.data}>"
