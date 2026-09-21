import os

from flask import Flask, render_template

from .extensions import db, login_manager
from .auth.routes import auth_bp
from .dashboard.routes import dashboard_bp
from .materi.routes import materi_bp
from .ujian.routes import ujian_bp
from .admin.routes import admin_bp
from .models import User, Subject, Material, Quiz, Question


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object("config.Config")
    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(materi_bp, url_prefix="/materi")
    app.register_blueprint(ujian_bp, url_prefix="/ujian")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    @app.get("/")
    def home():
        # Statistik nyata dari database.
        total_students = User.query.filter_by(role="siswa").count()
        total_subjects = Subject.query.filter_by(aktif=True).count()
        total_materials = Material.query.filter_by(aktif=True).count()

        # Hanya menghitung soal dari quiz yang masih aktif.
        total_questions = (
            db.session.query(Question)
            .join(Quiz, Question.quiz_id == Quiz.id)
            .filter(Quiz.aktif.is_(True))
            .count()
        )

        # Beberapa mata pelajaran aktif untuk kartu "Materi Populer".
        popular_subjects = (
            Subject.query
            .filter_by(aktif=True)
            .order_by(Subject.id.desc())
            .limit(3)
            .all()
        )

        # Satu soal aktif untuk mini quiz di landing page.
        quiz_question = (
            Question.query
            .join(Quiz, Question.quiz_id == Quiz.id)
            .filter(Quiz.aktif.is_(True))
            .order_by(Question.id.desc())
            .first()
        )

        return render_template(
            "index.html",
            total_students=total_students,
            total_subjects=total_subjects,
            total_materials=total_materials,
            total_questions=total_questions,
            popular_subjects=popular_subjects,
            quiz_question=quiz_question,
        )

    with app.app_context():
        db.create_all()

    return app
