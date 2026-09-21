# Banua Edu Flask v2

Versi ini menambahkan fondasi database untuk:
- pengguna dan role
- mata pelajaran
- materi
- ujian
- soal pilihan ganda
- pengerjaan ujian
- nilai/hasil ujian
- panel admin sederhana

## Jalankan di Windows 11

```powershell
py -3.11 -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python seed.py
python run.py
```

Buka `http://127.0.0.1:5000`

### Akun admin awal
- Username: `admin`
- Password: `admin123`

Setelah berhasil masuk, ganti password admin sebelum dipakai online.

## Alur pengembangan
1. Login/register
2. Admin membuat mata pelajaran
3. Admin menambahkan materi
4. Admin membuat ujian
5. Admin menambahkan soal
6. Siswa mengerjakan ujian
7. Sistem menghitung nilai otomatis

## cPanel
Gunakan Python 3.11. Untuk MySQL, install `PyMySQL` lalu isi `DATABASE_URL` di environment cPanel.

WSGI:
```python
import sys
project_home = "/home/USERNAME/banua_edu"
if project_home not in sys.path:
    sys.path.insert(0, project_home)
from app import create_app
application = create_app()
```
