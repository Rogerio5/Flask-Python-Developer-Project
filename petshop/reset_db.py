import os
from app import create_app, db
from app.models import Usuario, Categoria

DB_PATH = "petshop.db"

def reset_db():
    # Apaga o banco antigo se existir
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("🗑️ Banco antigo removido.")

    app = create_app()
    with app.app_context():
        # Garante que não sobra tabela antiga
        db.drop_all()
        db.create_all()
        print("📦 Tabelas recriadas.")

        # Cria usuário admin
        admin = Usuario(username="admin")
        admin.set_password("admin")
        db.session.add(admin)
        print("✅ Usuário admin criado (login: admin / senha: admin)")

        # Cria categorias iniciais
        categorias_iniciais = ["Cachorro", "Gato", "Coelho"]
        for nome in categorias_iniciais:
            db.session.add(Categoria(nome=nome, ativo=True))
            print(f"✅ Categoria '{nome}' criada")

        db.session.commit()
        print("🎉 Banco resetado com sucesso!")

if __name__ == "__main__":
    reset_db()
