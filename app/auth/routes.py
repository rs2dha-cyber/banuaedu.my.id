from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from ..extensions import db
from ..models import User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("dashboard.index"))
        flash("Username atau password salah.", "danger")
    return render_template("auth/login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nama = request.form.get("nama", "").strip()
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if not nama or not username or not password:
            flash("Semua field wajib diisi.", "danger")
            return render_template("auth/register.html")
        if User.query.filter_by(username=username).first():
            flash("Username sudah digunakan.", "danger")
            return render_template("auth/register.html")
        user = User(nama=nama, username=username, role="siswa")
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("Pendaftaran berhasil. Silakan masuk.", "success")
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html")

@auth_bp.get("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))
