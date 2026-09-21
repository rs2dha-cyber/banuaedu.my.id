from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from functools import wraps

from ..extensions import db
from ..models import (
    User,
    Subject,
    Material,
    Quiz,
    Question,
    Attempt
)


admin_bp = Blueprint("admin", __name__)


# ============================================================
# ADMIN REQUIRED
# ============================================================

def admin_required(fn):

    @wraps(fn)
    @login_required
    def wrapper(*args, **kwargs):

        if current_user.role != "admin":
            return "403 - Akses admin diperlukan.", 403

        return fn(*args, **kwargs)

    return wrapper


# ============================================================
# DASHBOARD ADMIN
# ============================================================

@admin_bp.get("/")
@admin_required
def index():

    return render_template(
        "admin/index.html",
        users=User.query.count(),
        subjects=Subject.query.count(),
        materials=Material.query.count(),
        quizzes=Quiz.query.count()
    )


# ============================================================
# ============================================================
# MATA PELAJARAN
# ============================================================
# ============================================================


# DAFTAR MATA PELAJARAN

@admin_bp.get("/subjects")
@admin_required
def subjects():

    subjects = (
        Subject.query
        .order_by(Subject.id.desc())
        .all()
    )

    return render_template(
        "admin/subjects.html",
        subjects=subjects
    )


# TAMBAH MATA PELAJARAN

@admin_bp.route(
    "/subject/new",
    methods=["GET", "POST"]
)
@admin_required
def new_subject():

    if request.method == "POST":

        nama = request.form.get(
            "nama",
            ""
        ).strip()

        jenjang = request.form.get(
            "jenjang",
            "SD • SMP • SMA"
        ).strip()

        deskripsi = request.form.get(
            "deskripsi",
            ""
        ).strip()

        if not nama:

            flash(
                "Nama mata pelajaran wajib diisi.",
                "danger"
            )

            return render_template(
                "admin/subject_form.html"
            )

        subject = Subject(
            nama=nama,
            jenjang=jenjang,
            deskripsi=deskripsi
        )

        db.session.add(subject)
        db.session.commit()

        flash(
            "Mata pelajaran berhasil ditambahkan.",
            "success"
        )

        return redirect(
            url_for("admin.subjects")
        )

    return render_template(
        "admin/subject_form.html"
    )


# EDIT MATA PELAJARAN

@admin_bp.route(
    "/subject/<int:subject_id>/edit",
    methods=["GET", "POST"]
)
@admin_required
def edit_subject(subject_id):

    subject = Subject.query.get_or_404(
        subject_id
    )

    if request.method == "POST":

        nama = request.form.get(
            "nama",
            ""
        ).strip()

        jenjang = request.form.get(
            "jenjang",
            ""
        ).strip()

        deskripsi = request.form.get(
            "deskripsi",
            ""
        ).strip()

        aktif = request.form.get("aktif")

        if not nama:

            flash(
                "Nama mata pelajaran wajib diisi.",
                "danger"
            )

            return render_template(
                "admin/subject_form.html",
                subject=subject,
                edit_mode=True
            )

        subject.nama = nama
        subject.jenjang = jenjang
        subject.deskripsi = deskripsi
        subject.aktif = aktif == "1"

        db.session.commit()

        flash(
            "Mata pelajaran berhasil diperbarui.",
            "success"
        )

        return redirect(
            url_for("admin.subjects")
        )

    return render_template(
        "admin/subject_form.html",
        subject=subject,
        edit_mode=True
    )


# HAPUS MATA PELAJARAN

@admin_bp.post(
    "/subject/<int:subject_id>/delete"
)
@admin_required
def delete_subject(subject_id):

    subject = Subject.query.get_or_404(
        subject_id
    )

    # Ambil semua materi
    materials = (
        Material.query
        .filter_by(
            subject_id=subject.id
        )
        .all()
    )

    # Ambil semua ujian
    quizzes = (
        Quiz.query
        .filter_by(
            subject_id=subject.id
        )
        .all()
    )

    # Hapus materi
    for material in materials:

        db.session.delete(material)

    # Hapus soal + attempt dari setiap ujian
    for quiz in quizzes:

        questions = (
            Question.query
            .filter_by(
                quiz_id=quiz.id
            )
            .all()
        )

        attempts = (
            Attempt.query
            .filter_by(
                quiz_id=quiz.id
            )
            .all()
        )

        for question in questions:
            db.session.delete(question)

        for attempt in attempts:
            db.session.delete(attempt)

        db.session.delete(quiz)

    db.session.delete(subject)

    db.session.commit()

    flash(
        "Mata pelajaran dan data terkait berhasil dihapus.",
        "success"
    )

    return redirect(
        url_for("admin.subjects")
    )


# ============================================================
# ============================================================
# MATERI
# ============================================================
# ============================================================


# DAFTAR MATERI

@admin_bp.get("/materials")
@admin_required
def materials():

    materials = (
        Material.query
        .order_by(
            Material.subject_id.asc(),
            Material.urutan.asc(),
            Material.id.desc()
        )
        .all()
    )

    return render_template(
        "admin/materials.html",
        materials=materials
    )


# TAMBAH MATERI

@admin_bp.route(
    "/material/new",
    methods=["GET", "POST"]
)
@admin_required
def new_material():

    subjects = (
        Subject.query
        .filter_by(aktif=True)
        .order_by(Subject.nama.asc())
        .all()
    )

    if request.method == "POST":

        subject_id = request.form.get(
            "subject_id",
            ""
        ).strip()

        judul = request.form.get(
            "judul",
            ""
        ).strip()

        isi = request.form.get(
            "isi",
            ""
        )

        video_url = request.form.get(
            "video_url",
            ""
        ).strip()

        pdf_url = request.form.get(
            "pdf_url",
            ""
        ).strip()

        urutan = request.form.get(
            "urutan",
            "1"
        ).strip()

        if not subject_id:

            flash(
                "Silakan pilih mata pelajaran.",
                "danger"
            )

            return render_template(
                "admin/material_form.html",
                subjects=subjects
            )

        if not judul:

            flash(
                "Judul materi wajib diisi.",
                "danger"
            )

            return render_template(
                "admin/material_form.html",
                subjects=subjects
            )

        try:

            subject_id = int(subject_id)
            urutan = int(urutan or 1)

        except ValueError:

            flash(
                "Data materi tidak valid.",
                "danger"
            )

            return render_template(
                "admin/material_form.html",
                subjects=subjects
            )

        subject = Subject.query.get(
            subject_id
        )

        if not subject:

            flash(
                "Mata pelajaran tidak ditemukan.",
                "danger"
            )

            return render_template(
                "admin/material_form.html",
                subjects=subjects
            )

        material = Material(
            subject_id=subject_id,
            judul=judul,
            isi=isi,
            video_url=video_url,
            pdf_url=pdf_url,
            urutan=urutan
        )

        db.session.add(material)
        db.session.commit()

        flash(
            "Materi berhasil ditambahkan.",
            "success"
        )

        return redirect(
            url_for("admin.materials")
        )

    return render_template(
        "admin/material_form.html",
        subjects=subjects
    )


# EDIT MATERI

@admin_bp.route(
    "/material/<int:material_id>/edit",
    methods=["GET", "POST"]
)
@admin_required
def edit_material(material_id):

    material = Material.query.get_or_404(
        material_id
    )

    subjects = (
        Subject.query
        .filter_by(aktif=True)
        .order_by(Subject.nama.asc())
        .all()
    )

    if request.method == "POST":

        subject_id = request.form.get(
            "subject_id",
            ""
        ).strip()

        judul = request.form.get(
            "judul",
            ""
        ).strip()

        isi = request.form.get(
            "isi",
            ""
        )

        video_url = request.form.get(
            "video_url",
            ""
        ).strip()

        pdf_url = request.form.get(
            "pdf_url",
            ""
        ).strip()

        urutan = request.form.get(
            "urutan",
            "1"
        ).strip()

        if not subject_id or not judul:

            flash(
                "Mata pelajaran dan judul wajib diisi.",
                "danger"
            )

            return render_template(
                "admin/material_form.html",
                subjects=subjects,
                material=material,
                edit_mode=True
            )

        try:

            subject_id = int(subject_id)
            urutan = int(urutan or 1)

        except ValueError:

            flash(
                "Data materi tidak valid.",
                "danger"
            )

            return render_template(
                "admin/material_form.html",
                subjects=subjects,
                material=material,
                edit_mode=True
            )

        material.subject_id = subject_id
        material.judul = judul
        material.isi = isi
        material.video_url = video_url
        material.pdf_url = pdf_url
        material.urutan = urutan

        db.session.commit()

        flash(
            "Materi berhasil diperbarui.",
            "success"
        )

        return redirect(
            url_for("admin.materials")
        )

    return render_template(
        "admin/material_form.html",
        subjects=subjects,
        material=material,
        edit_mode=True
    )


# HAPUS MATERI

@admin_bp.post(
    "/material/<int:material_id>/delete"
)
@admin_required
def delete_material(material_id):

    material = Material.query.get_or_404(
        material_id
    )

    db.session.delete(material)
    db.session.commit()

    flash(
        "Materi berhasil dihapus.",
        "success"
    )

    return redirect(
        url_for("admin.materials")
    )


# ============================================================
# ============================================================
# UJIAN
# ============================================================
# ============================================================


# DAFTAR UJIAN

@admin_bp.get("/quizzes")
@admin_required
def quizzes():

    quizzes = (
        Quiz.query
        .order_by(Quiz.id.desc())
        .all()
    )

    return render_template(
        "admin/quizzes.html",
        quizzes=quizzes
    )


# TAMBAH UJIAN

@admin_bp.route(
    "/quiz/new",
    methods=["GET", "POST"]
)
@admin_required
def new_quiz():

    subjects = (
        Subject.query
        .filter_by(aktif=True)
        .order_by(Subject.nama.asc())
        .all()
    )

    if request.method == "POST":

        subject_id = request.form.get(
            "subject_id",
            ""
        ).strip()

        judul = request.form.get(
            "judul",
            ""
        ).strip()

        durasi = request.form.get(
            "durasi",
            "30"
        ).strip()

        if not subject_id:

            flash(
                "Silakan pilih mata pelajaran.",
                "danger"
            )

            return render_template(
                "admin/quiz_form.html",
                subjects=subjects
            )

        if not judul:

            flash(
                "Judul ujian wajib diisi.",
                "danger"
            )

            return render_template(
                "admin/quiz_form.html",
                subjects=subjects
            )

        try:

            subject_id = int(subject_id)
            durasi = int(durasi)

        except ValueError:

            flash(
                "Data ujian tidak valid.",
                "danger"
            )

            return render_template(
                "admin/quiz_form.html",
                subjects=subjects
            )

        if durasi < 1:

            flash(
                "Durasi ujian minimal 1 menit.",
                "danger"
            )

            return render_template(
                "admin/quiz_form.html",
                subjects=subjects
            )

        subject = Subject.query.get(
            subject_id
        )

        if not subject:

            flash(
                "Mata pelajaran tidak ditemukan.",
                "danger"
            )

            return render_template(
                "admin/quiz_form.html",
                subjects=subjects
            )

        quiz = Quiz(
            subject_id=subject_id,
            judul=judul,
            durasi_menit=durasi
        )

        db.session.add(quiz)
        db.session.commit()

        flash(
            "Ujian berhasil dibuat.",
            "success"
        )

        return redirect(
            url_for("admin.quizzes")
        )

    return render_template(
        "admin/quiz_form.html",
        subjects=subjects
    )


# EDIT UJIAN

@admin_bp.route(
    "/quiz/<int:quiz_id>/edit",
    methods=["GET", "POST"]
)
@admin_required
def edit_quiz(quiz_id):

    quiz = Quiz.query.get_or_404(
        quiz_id
    )

    subjects = (
        Subject.query
        .filter_by(aktif=True)
        .order_by(Subject.nama.asc())
        .all()
    )

    if request.method == "POST":

        subject_id = request.form.get(
            "subject_id",
            ""
        ).strip()

        judul = request.form.get(
            "judul",
            ""
        ).strip()

        durasi = request.form.get(
            "durasi",
            "30"
        ).strip()

        if not subject_id or not judul:

            flash(
                "Mata pelajaran dan judul wajib diisi.",
                "danger"
            )

            return render_template(
                "admin/quiz_form.html",
                subjects=subjects,
                quiz=quiz,
                edit_mode=True
            )

        try:

            subject_id = int(subject_id)
            durasi = int(durasi)

        except ValueError:

            flash(
                "Data ujian tidak valid.",
                "danger"
            )

            return render_template(
                "admin/quiz_form.html",
                subjects=subjects,
                quiz=quiz,
                edit_mode=True
            )

        if durasi < 1:

            flash(
                "Durasi minimal 1 menit.",
                "danger"
            )

            return render_template(
                "admin/quiz_form.html",
                subjects=subjects,
                quiz=quiz,
                edit_mode=True
            )

        quiz.subject_id = subject_id
        quiz.judul = judul
        quiz.durasi_menit = durasi

        db.session.commit()

        flash(
            "Ujian berhasil diperbarui.",
            "success"
        )

        return redirect(
            url_for("admin.quizzes")
        )

    return render_template(
        "admin/quiz_form.html",
        subjects=subjects,
        quiz=quiz,
        edit_mode=True
    )


# HAPUS UJIAN

@admin_bp.post(
    "/quiz/<int:quiz_id>/delete"
)
@admin_required
def delete_quiz(quiz_id):

    quiz = Quiz.query.get_or_404(
        quiz_id
    )

    questions = (
        Question.query
        .filter_by(
            quiz_id=quiz.id
        )
        .all()
    )

    attempts = (
        Attempt.query
        .filter_by(
            quiz_id=quiz.id
        )
        .all()
    )

    for question in questions:

        db.session.delete(question)

    for attempt in attempts:

        db.session.delete(attempt)

    db.session.delete(quiz)

    db.session.commit()

    flash(
        "Ujian beserta soal dan hasil terkait berhasil dihapus.",
        "success"
    )

    return redirect(
        url_for("admin.quizzes")
    )


# ============================================================
# ============================================================
# SOAL
# ============================================================
# ============================================================


# DAFTAR SOAL

@admin_bp.get("/questions")
@admin_required
def questions():

    questions = (
        Question.query
        .order_by(Question.id.desc())
        .all()
    )

    return render_template(
        "admin/questions.html",
        questions=questions
    )


# TAMBAH SOAL

@admin_bp.route(
    "/question/new",
    methods=["GET", "POST"]
)
@admin_required
def new_question():

    quizzes = (
        Quiz.query
        .order_by(Quiz.id.desc())
        .all()
    )

    if request.method == "POST":

        quiz_id = request.form.get(
            "quiz_id",
            ""
        ).strip()

        pertanyaan = request.form.get(
            "pertanyaan",
            ""
        ).strip()

        opsi_a = request.form.get(
            "opsi_a",
            ""
        ).strip()

        opsi_b = request.form.get(
            "opsi_b",
            ""
        ).strip()

        opsi_c = request.form.get(
            "opsi_c",
            ""
        ).strip()

        opsi_d = request.form.get(
            "opsi_d",
            ""
        ).strip()

        jawaban = request.form.get(
            "jawaban",
            ""
        ).strip().lower()

        if not quiz_id:

            flash(
                "Silakan pilih ujian.",
                "danger"
            )

            return render_template(
                "admin/question_form.html",
                quizzes=quizzes
            )

        if not pertanyaan:

            flash(
                "Pertanyaan wajib diisi.",
                "danger"
            )

            return render_template(
                "admin/question_form.html",
                quizzes=quizzes
            )

        if not opsi_a or not opsi_b or not opsi_c or not opsi_d:

            flash(
                "Pilihan A, B, C, dan D wajib diisi.",
                "danger"
            )

            return render_template(
                "admin/question_form.html",
                quizzes=quizzes
            )

        if jawaban not in [
            "a",
            "b",
            "c",
            "d"
        ]:

            flash(
                "Jawaban benar harus A, B, C, atau D.",
                "danger"
            )

            return render_template(
                "admin/question_form.html",
                quizzes=quizzes
            )

        try:

            quiz_id = int(quiz_id)

        except ValueError:

            flash(
                "Ujian tidak valid.",
                "danger"
            )

            return render_template(
                "admin/question_form.html",
                quizzes=quizzes
            )

        quiz = Quiz.query.get(
            quiz_id
        )

        if not quiz:

            flash(
                "Ujian tidak ditemukan.",
                "danger"
            )

            return render_template(
                "admin/question_form.html",
                quizzes=quizzes
            )

        question = Question(
            quiz_id=quiz_id,
            pertanyaan=pertanyaan,
            opsi_a=opsi_a,
            opsi_b=opsi_b,
            opsi_c=opsi_c,
            opsi_d=opsi_d,
            jawaban=jawaban
        )

        db.session.add(question)
        db.session.commit()

        flash(
            "Soal berhasil ditambahkan.",
            "success"
        )

        return redirect(
            url_for("admin.questions")
        )

    return render_template(
        "admin/question_form.html",
        quizzes=quizzes
    )


# EDIT SOAL

@admin_bp.route(
    "/question/<int:question_id>/edit",
    methods=["GET", "POST"]
)
@admin_required
def edit_question(question_id):

    question = Question.query.get_or_404(
        question_id
    )

    quizzes = (
        Quiz.query
        .order_by(Quiz.id.desc())
        .all()
    )

    if request.method == "POST":

        quiz_id = request.form.get(
            "quiz_id",
            ""
        ).strip()

        pertanyaan = request.form.get(
            "pertanyaan",
            ""
        ).strip()

        opsi_a = request.form.get(
            "opsi_a",
            ""
        ).strip()

        opsi_b = request.form.get(
            "opsi_b",
            ""
        ).strip()

        opsi_c = request.form.get(
            "opsi_c",
            ""
        ).strip()

        opsi_d = request.form.get(
            "opsi_d",
            ""
        ).strip()

        jawaban = request.form.get(
            "jawaban",
            ""
        ).strip().lower()

        if not quiz_id or not pertanyaan:

            flash(
                "Ujian dan pertanyaan wajib diisi.",
                "danger"
            )

            return render_template(
                "admin/question_form.html",
                quizzes=quizzes,
                question=question,
                edit_mode=True
            )

        if not opsi_a or not opsi_b or not opsi_c or not opsi_d:

            flash(
                "Pilihan A, B, C, dan D wajib diisi.",
                "danger"
            )

            return render_template(
                "admin/question_form.html",
                quizzes=quizzes,
                question=question,
                edit_mode=True
            )

        if jawaban not in [
            "a",
            "b",
            "c",
            "d"
        ]:

            flash(
                "Jawaban benar harus A, B, C, atau D.",
                "danger"
            )

            return render_template(
                "admin/question_form.html",
                quizzes=quizzes,
                question=question,
                edit_mode=True
            )

        try:

            quiz_id = int(quiz_id)

        except ValueError:

            flash(
                "Ujian tidak valid.",
                "danger"
            )

            return render_template(
                "admin/question_form.html",
                quizzes=quizzes,
                question=question,
                edit_mode=True
            )

        question.quiz_id = quiz_id
        question.pertanyaan = pertanyaan
        question.opsi_a = opsi_a
        question.opsi_b = opsi_b
        question.opsi_c = opsi_c
        question.opsi_d = opsi_d
        question.jawaban = jawaban

        db.session.commit()

        flash(
            "Soal berhasil diperbarui.",
            "success"
        )

        return redirect(
            url_for("admin.questions")
        )

    return render_template(
        "admin/question_form.html",
        quizzes=quizzes,
        question=question,
        edit_mode=True
    )


# HAPUS SOAL

@admin_bp.post(
    "/question/<int:question_id>/delete"
)
@admin_required
def delete_question(question_id):

    question = Question.query.get_or_404(
        question_id
    )

    db.session.delete(question)

    db.session.commit()

    flash(
        "Soal berhasil dihapus.",
        "success"
    )

    return redirect(
        url_for("admin.questions")
    )