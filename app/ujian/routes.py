from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from ..models import Quiz, Question, Attempt
from ..extensions import db

from datetime import datetime


ujian_bp = Blueprint("ujian", __name__)


# =========================================================
# DAFTAR UJIAN
# =========================================================
@ujian_bp.get("/")
@login_required
def index():
    quizzes = (
        Quiz.query
        .filter_by(aktif=True)
        .order_by(Quiz.id.desc())
        .all()
    )

    return render_template(
        "ujian/index.html",
        quizzes=quizzes
    )


# =========================================================
# MENGERJAKAN UJIAN
# =========================================================
@ujian_bp.route("/<int:quiz_id>", methods=["GET", "POST"])
@login_required
def take(quiz_id):

    quiz = Quiz.query.get_or_404(quiz_id)

    questions = (
        Question.query
        .filter_by(quiz_id=quiz.id)
        .order_by(Question.id)
        .all()
    )

    # -----------------------------------------------------
    # KETIKA SISWA MENEKAN "KIRIM JAWABAN"
    # -----------------------------------------------------
    if request.method == "POST":

        benar = 0

        # Periksa setiap soal
        for q in questions:

            # Jawaban yang dipilih siswa
            jawaban_user = (
                request.form.get(f"q{q.id}", "")
                .strip()
                .lower()
            )

            # Jawaban benar dari database
            jawaban_benar = (
                q.jawaban or ""
            ).strip().lower()

            # Bandingkan
            if jawaban_user == jawaban_benar:
                benar += 1

        # Jumlah seluruh soal
        total = len(questions)

        # Hitung nilai
        if total > 0:
            nilai = round((benar / total) * 100, 2)
        else:
            nilai = 0

        # Simpan hasil ujian
        attempt = Attempt(
            user_id=current_user.id,
            quiz_id=quiz.id,
            nilai=nilai,
            benar=benar,
            total=total,
            selesai_at=datetime.utcnow()
        )

        db.session.add(attempt)
        db.session.commit()

        # Tampilkan halaman hasil
        return redirect(
            url_for(
                "ujian.result",
                quiz_id=quiz.id
            )
        )

    # -----------------------------------------------------
    # TAMPILKAN HALAMAN SOAL
    # -----------------------------------------------------
    return render_template(
        "ujian/take.html",
        quiz=quiz,
        questions=questions
    )


# =========================================================
# HASIL UJIAN
# =========================================================
@ujian_bp.get("/result/<int:quiz_id>")
@login_required
def result(quiz_id):

    quiz = Quiz.query.get_or_404(quiz_id)

    # Ambil hasil ujian terakhir siswa
    attempt = (
        Attempt.query
        .filter_by(
            user_id=current_user.id,
            quiz_id=quiz_id
        )
        .order_by(Attempt.id.desc())
        .first()
    )

    if not attempt:
        flash(
            "Hasil ujian belum tersedia.",
            "danger"
        )

        return redirect(
            url_for("ujian.index")
        )

    return render_template(
        "ujian/result.html",
        quiz=quiz,
        attempt=attempt,
        questions=(
            Question.query
            .filter_by(quiz_id=quiz.id)
            .order_by(Question.id.asc())
            .all()
        ),
    )