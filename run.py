"""
Banua Edu - Application Runner

File ini menjalankan Flask melalui application factory `create_app()`.
- Port tetap 5000 agar sesuai dengan Cloudflare Tunnel BanuaEdu.
- Debug aktif agar perubahan kode di VS Code dapat ter-reload saat development.
- Import path dibuat fleksibel agar tetap bekerja jika folder `app`
  berada langsung di sebelah run.py atau berada di dalam folder `banua_edu`.
"""

from pathlib import Path
import os
import sys

# Folder tempat file run.py berada.
BASE_DIR = Path(__file__).resolve().parent

# Dukung dua kemungkinan struktur:
# 1) project/app/...
# 2) project/banua_edu/app/...
possible_app_roots = [
    BASE_DIR,
    BASE_DIR / "banua_edu",
]

for root in possible_app_roots:
    if (root / "app").is_dir():
        root_str = str(root)
        if root_str not in sys.path:
            sys.path.insert(0, root_str)
        break

from app import create_app  # noqa: E402


# Buat instance Flask dari application factory.
app = create_app()


if __name__ == "__main__":
    # Default development mode.
    # BANUA_DEBUG=0 dapat digunakan untuk menjalankan tanpa debug/reloader.
    debug = os.getenv("BANUA_DEBUG", "1").strip().lower() not in {
        "0", "false", "no", "off"
    }

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=debug,
        use_reloader=debug,
    )
