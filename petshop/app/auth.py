from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash, generate_password_hash

auth_bp = Blueprint("auth", __name__)

# Usuários de exemplo (em produção use banco de dados)
USERS = {
    "admin": generate_password_hash("admin"),       # login: admin / senha: admin
    "rogerio": generate_password_hash("senha123")   # login: rogerio / senha: senha123
}

@auth_bp.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user_hash = USERS.get(username)
        if user_hash and check_password_hash(user_hash, password):
            session["user"] = username
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for("main.home"))  # redireciona para a home
        else:
            flash("Usuário ou senha inválidos", "danger")
            return redirect(url_for("auth.login_page"))

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.pop("user", None)
    flash("Você saiu da conta.", "info")
    return redirect(url_for("auth.login_page"))
