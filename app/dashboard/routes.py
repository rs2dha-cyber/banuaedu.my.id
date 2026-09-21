from flask import Blueprint, render_template
from flask_login import login_required, current_user

from ..models import Subject, Material, Quiz, Attempt


dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.get("/dashboard")
@login_required
def index():

    # =====================================================
    # DATA DASAR
    # =====================================================

    total_materi = (
        Material.query
        .filter_by(aktif=True)
        .count()
    )

    total_ujian = (
        Quiz.query
        .filter_by(aktif=True)
        .count()
    )


    # =====================================================
    # MATA PELAJARAN
    # =====================================================

    subjects = (
        Subject.query
        .filter_by(aktif=True)
        .order_by(Subject.nama.asc())
        .all()
    )


    # =====================================================
    # MATERI TERBARU
    # =====================================================

    materials = (
        Material.query
        .filter_by(aktif=True)
        .order_by(
            Material.id.desc()
        )
        .limit(6)
        .all()
    )


    # =====================================================
    # UJIAN TERBARU
    # =====================================================

    quizzes = (
        Quiz.query
        .filter_by(aktif=True)
        .order_by(
            Quiz.id.desc()
        )
        .limit(5)
        .all()
    )


    # =====================================================
    # HASIL UJIAN SISWA
    # =====================================================

    attempts = (
        Attempt.query
        .filter_by(
            user_id=current_user.id
        )
        .order_by(
            Attempt.id.desc()
        )
        .all()
    )


    # =====================================================
    # NILAI RATA-RATA
    # =====================================================

    if attempts:

        rata_rata = round(
            sum(
                a.nilai
                for a in attempts
            ) / len(attempts),
            2
        )

    else:

        rata_rata = 0


    # =====================================================
    # NILAI TERBAIK
    # =====================================================

    if attempts:

        nilai_terbaik = max(
            a.nilai
            for a in attempts
        )

    else:

        nilai_terbaik = 0


    # =====================================================
    # JUMLAH UJIAN SELESAI
    # =====================================================

    ujian_selesai = len(attempts)


    # =====================================================
    # PROGRESS UJIAN
    # =====================================================

    if total_ujian > 0:

        progress = round(
            (ujian_selesai / total_ujian) * 100
        )

        progress = min(
            progress,
            100
        )

    else:

        progress = 0


    # =====================================================
    # UJIAN TERAKHIR
    # =====================================================

    ujian_terakhir = (
        attempts[0]
        if attempts
        else None
    )


    # =====================================================
    # RENDER DASHBOARD
    # =====================================================

    return render_template(
        "dashboard/index.html",

        user=current_user,

        subjects=subjects,

        materials=materials,

        quizzes=quizzes,

        total_materi=total_materi,

        total_ujian=total_ujian,

        ujian_selesai=ujian_selesai,

        rata_rata=rata_rata,

        nilai_terbaik=nilai_terbaik,

        progress=progress,

        ujian_terakhir=ujian_terakhir
    )