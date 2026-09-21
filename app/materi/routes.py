from flask import Blueprint, render_template
from flask_login import login_required

from ..models import Subject, Material


materi_bp = Blueprint("materi", __name__)


# =========================================================
# DAFTAR MATA PELAJARAN
# =========================================================
@materi_bp.get("/")
@login_required
def index():

    subjects = (
        Subject.query
        .filter_by(aktif=True)
        .order_by(Subject.nama.asc())
        .all()
    )

    return render_template(
        "materi/index.html",
        subjects=subjects
    )


# =========================================================
# DAFTAR MATERI BERDASARKAN MATA PELAJARAN
# =========================================================
@materi_bp.get("/subject/<int:subject_id>")
@login_required
def subject_detail(subject_id):

    subject = Subject.query.get_or_404(subject_id)

    materials = (
        Material.query
        .filter_by(
            subject_id=subject_id,
            aktif=True
        )
        .order_by(
            Material.urutan.asc(),
            Material.id.asc()
        )
        .all()
    )

    return render_template(
        "materi/subject.html",
        subject=subject,
        materials=materials
    )


# =========================================================
# DETAIL MATERI
# =========================================================
@materi_bp.get("/material/<int:material_id>")
@login_required
def detail(material_id):

    # Ambil materi
    item = Material.query.get_or_404(material_id)

    # Ambil mata pelajaran
    subject = Subject.query.get_or_404(
        item.subject_id
    )

    # Ambil semua materi aktif dalam mata pelajaran yang sama
    materials = (
        Material.query
        .filter_by(
            subject_id=item.subject_id,
            aktif=True
        )
        .order_by(
            Material.urutan.asc(),
            Material.id.asc()
        )
        .all()
    )

    # -----------------------------------------------------
    # Cari posisi materi yang sedang dibuka
    # -----------------------------------------------------

    current_index = -1

    for index, material in enumerate(materials):

        if material.id == item.id:
            current_index = index
            break


    # -----------------------------------------------------
    # Materi sebelumnya
    # -----------------------------------------------------

    prev_material = None

    if current_index > 0:

        prev_material = materials[
            current_index - 1
        ]


    # -----------------------------------------------------
    # Materi berikutnya
    # -----------------------------------------------------

    next_material = None

    if (
        current_index >= 0
        and current_index < len(materials) - 1
    ):

        next_material = materials[
            current_index + 1
        ]


    # -----------------------------------------------------
    # Kirim semua data ke template
    # -----------------------------------------------------

    return render_template(
        "materi/detail.html",

        item=item,

        subject=subject,

        prev_material=prev_material,

        next_material=next_material
    )