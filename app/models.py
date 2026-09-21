from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .extensions import db, login_manager
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="siswa", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(120), nullable=False)
    jenjang = db.Column(db.String(50), default="SD • SMP • SMA")
    deskripsi = db.Column(db.Text, default="")
    aktif = db.Column(db.Boolean, default=True)
    materials = db.relationship("Material", backref="subject", lazy=True, cascade="all, delete-orphan")
    quizzes = db.relationship("Quiz", backref="subject", lazy=True, cascade="all, delete-orphan")

class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey("subject.id"), nullable=False)
    judul = db.Column(db.String(180), nullable=False)
    isi = db.Column(db.Text, default="")
    video_url = db.Column(db.String(500), default="")
    pdf_url = db.Column(db.String(500), default="")
    urutan = db.Column(db.Integer, default=1)
    aktif = db.Column(db.Boolean, default=True)

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey("subject.id"), nullable=False)
    judul = db.Column(db.String(180), nullable=False)
    durasi_menit = db.Column(db.Integer, default=30)
    aktif = db.Column(db.Boolean, default=True)
    questions = db.relationship("Question", backref="quiz", lazy=True, cascade="all, delete-orphan")

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id"), nullable=False)
    pertanyaan = db.Column(db.Text, nullable=False)
    opsi_a = db.Column(db.Text, nullable=False)
    opsi_b = db.Column(db.Text, nullable=False)
    opsi_c = db.Column(db.Text, nullable=False)
    opsi_d = db.Column(db.Text, nullable=False)
    jawaban = db.Column(db.String(1), nullable=False)
    pembahasan = db.Column(db.Text, default="")

class Attempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id"), nullable=False)
    nilai = db.Column(db.Float, default=0)
    benar = db.Column(db.Integer, default=0)
    total = db.Column(db.Integer, default=0)
    selesai_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship("User", backref="attempts")
    quiz = db.relationship("Quiz", backref="attempts")

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
