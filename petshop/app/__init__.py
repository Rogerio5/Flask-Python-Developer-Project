from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import datetime

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "chave-secreta"  # troque por algo seguro
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///petshop.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from .models import Usuario

    # Configuração do Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = "auth.login_page"  # rota de login
    login_manager.login_message = "Por favor, faça login para acessar esta página."
    login_manager.login_message_category = "warning"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    # Blueprints
    from .routes import bp as main_bp
    from .auth import auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    # Contexto global (ex: ano atual no rodapé)
    @app.context_processor
    def inject_now():
        return {"current_year": datetime.now().year}

    return app

__all__ = ["create_app", "db"]

