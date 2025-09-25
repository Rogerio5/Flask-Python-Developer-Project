from app import create_app, db
from app.models import Usuario, Categoria

app = create_app()

with app.app_context():
    # Cria todas as tabelas
    db.create_all()

    # Cria usuário admin se não existir
    if not Usuario.query.filter_by(username="admin").first():
        admin = Usuario(username="admin")
        admin.set_password("admin")
        db.session.add(admin)
        print("✅ Usuário admin criado (login: admin / senha: admin)")
    else:
        print("ℹ️ Usuário admin já existe.")

    # Cria categorias iniciais se não existirem
    categorias_iniciais = ["Cachorro", "Gato", "Coelho"]
    for nome in categorias_iniciais:
        if not Categoria.query.filter_by(nome=nome).first():
            db.session.add(Categoria(nome=nome, ativo=True))
            print(f"✅ Categoria '{nome}' criada")
        else:
            print(f"ℹ️ Categoria '{nome}' já existe.")

    # Salva no banco
    db.session.commit()
    print("🎉 Banco inicializado com sucesso!")
