from app import create_app
from app.extensions import db
from app.models import User, Subject, Material, Quiz, Question

app = create_app()
with app.app_context():
    if not User.query.filter_by(username="admin").first():
        u = User(nama="Administrator Banua Edu", username="admin", role="admin")
        u.set_password("admin123")
        db.session.add(u)

    names = [
        ("Matematika", "SD • SMP • SMA", "Pembelajaran matematika bertahap dari dasar hingga lanjutan."),
        ("Bahasa Indonesia", "SD • SMP • SMA", "Literasi, membaca, menulis, dan apresiasi sastra."),
        ("Bahasa Inggris", "SD • SMP • SMA", "Vocabulary, grammar, reading, dan conversation."),
        ("IPA", "SD • SMP • SMA", "Sains, eksperimen sederhana, dan alam sekitar."),
        ("IPS", "SD • SMP • SMA", "Sejarah, geografi, ekonomi, dan budaya lokal Banua."),
        ("Informatika", "SMP • SMA • SMK", "Komputer, internet, dan pemrograman dasar."),
    ]
    for nama, jenjang, deskripsi in names:
        if not Subject.query.filter(db.func.lower(Subject.nama) == nama.lower()).first():
            db.session.add(Subject(nama=nama, jenjang=jenjang, deskripsi=deskripsi))
    db.session.commit()

    # --- Materi lengkap per mapel ---
    subj = {s.nama: s for s in Subject.query.all()}

    materials_data = [
            # Matematika
            (subj["Matematika"].id, "Bilangan Dasar", """
<h3>Pengenalan Bilangan</h3>
<p>Bilangan adalah dasar semua perhitungan. Kita mengenal bilangan asli (1, 2, 3, …), bilangan bulat, dan pecahan.</p>
<ul>
<li><strong>Penjumlahan (+)</strong> — menggabungkan nilai</li>
<li><strong>Pengurangan (−)</strong> — mengurangi nilai</li>
<li><strong>Perkalian (×)</strong> — penjumlahan berulang</li>
<li><strong>Pembagian (÷)</strong> — membagi rata</li>
</ul>
<p>Latihan: 12 + 8 = 20, 15 − 7 = 8, 6 × 4 = 24, 20 ÷ 5 = 4.</p>
<p><em>Tips Banua:</em> Hitung sambil membayangkan jumlah buah rambutan di pasar Barabai — lebih mudah diingat!</p>
""", 1),
            (subj["Matematika"].id, "Pecahan dan Desimal", """
<h3>Pecahan</h3>
<p>Pecahan menyatakan bagian dari keseluruhan, misalnya 1/2, 3/4. Desimal adalah bentuk lain: 0,5 = 1/2.</p>
<p>Operasi penting: menyamakan penyebut, menyederhanakan, dan mengubah ke desimal/persen.</p>
""", 2),
            (subj["Matematika"].id, "Persentase & Perbandingan", """
<h3>Persentase</h3>
<p>Persen (%) = per seratus. Contoh: 25% dari 80 = 20. Perbandingan membandingkan dua kuantitas (a : b).</p>
""", 3),

            # Bahasa Indonesia
            (subj["Bahasa Indonesia"].id, "Membaca & Memahami Teks", """
<h3>Strategi Membaca</h3>
<p>Bacalah judul dan paragraf pertama, cari gagasan utama, lalu catat kata kunci. Bedakan fakta dan opini.</p>
<p>Contoh teks lokal: cerita pasar terapung atau legenda Meratus dapat dilatih untuk menemukan ide pokok.</p>
""", 1),
            (subj["Bahasa Indonesia"].id, "Menulis Paragraf", """
<h3>Struktur Paragraf</h3>
<p>Setiap paragraf idealnya punya kalimat topik, kalimat penjelas, dan penutup. Gunakan ejaan yang benar (EYD/PUEBI).</p>
""", 2),
            (subj["Bahasa Indonesia"].id, "Sastra & Pantun Banjar", """
<h3>Apresiasi Sastra</h3>
<p>Pantun Banjar dan syair lokal memperkaya literasi. Perhatikan rima, pesan moral, dan kosa kata daerah yang sopan.</p>
""", 3),

            # Bahasa Inggris
            (subj["Bahasa Inggris"].id, "Basic Vocabulary", """
<h3>Everyday Words</h3>
<p>Learn common nouns, verbs, and adjectives. Example: river = sungai, market = pasar, learn = belajar.</p>
<p>Practice sentences: “I live in Barabai.” “We study every day.”</p>
""", 1),
            (subj["Bahasa Inggris"].id, "Simple Present & Past", """
<h3>Tenses</h3>
<p>Simple Present: habits (I study). Simple Past: finished actions (I studied yesterday). Watch verb forms (go → went).</p>
""", 2),

            # IPA
            (subj["IPA"].id, "Makhluk Hidup & Lingkungan", """
<h3>Ciri Makhluk Hidup</h3>
<p>Bernapas, bergerak, berkembang biak, dan membutuhkan nutrisi. Lingkungan hidup di Kalimantan kaya hutan dan sungai.</p>
<p>Jaga kebersihan sungai agar ekosistem tetap sehat — contoh nyata di sekitar Barabai.</p>
""", 1),
            (subj["IPA"].id, "Gaya, Gerak & Energi", """
<h3>Gaya dan Gerak</h3>
<p>Gaya mendorong atau menarik benda. Energi bisa kinetik, potensial, panas, dan listrik. Hukum sederhana Newton membantu memahami gerak sehari-hari.</p>
""", 2),
            (subj["IPA"].id, "Bumi & Antariksa", """
<h3>Sistem Tata Surya</h3>
<p>Matahari sebagai pusat, planet mengelilinginya. Bumi memiliki atmosfer yang melindungi kehidupan. Kenali fase bulan dan gerhana secara sederhana.</p>
""", 3),

            # IPS
            (subj["IPS"].id, "Geografi Kalimantan Selatan", """
<h3>Wilayah & Karakteristik</h3>
<p>Kalimantan Selatan memiliki dataran rendah, rawa, sungai besar, dan Pegunungan Meratus. Kabupaten Hulu Sungai Tengah beribukota <strong>Barabai</strong>.</p>
<ul>
<li>Barabai dijuluki “Kota Intan”</li>
<li>Sungai penting bagi transportasi dan ekonomi</li>
<li>Budaya Banjar: gotong royong, pasar, dan seni sasirangan</li>
</ul>
""", 1),
            (subj["IPS"].id, "Sejarah Lokal Banua", """
<h3>Jejak Sejarah</h3>
<p>Kerajaan Banjar, jalur perdagangan sungai, dan peran masyarakat Hulu Sungai dalam perdagangan hasil bumi membentuk identitas daerah. Hargai sejarah agar cinta tanah air tumbuh.</p>
""", 2),
            (subj["IPS"].id, "Ekonomi & Kewirausahaan Sederhana", """
<h3>Kegiatan Ekonomi</h3>
<p>Produksi, distribusi, konsumsi. Di Barabai dan sekitarnya: pertanian, perdagangan pasar, dan kerajinan. Kewirausahaan dimulai dari ide kecil yang bermanfaat.</p>
""", 3),

            # Informatika
            (subj["Informatika"].id, "Pengenalan Komputer", """
<h3>Hardware & Software</h3>
<p>Hardware: CPU, RAM, storage, input/output. Software: sistem operasi dan aplikasi. Jaga perangkat dengan update dan antivirus dasar.</p>
""", 1),
            (subj["Informatika"].id, "Internet & Keamanan Digital", """
<h3>Internet Sehat</h3>
<p>Gunakan kata sandi kuat, jangan bagikan data pribadi, waspadai hoaks. Manfaatkan internet untuk belajar materi Banua Edu dan sumber terpercaya.</p>
""", 2),
            (subj["Informatika"].id, "Algoritma Dasar", """
<h3>Berpikir Komputasional</h3>
<p>Algoritma = langkah-langkah terurut menyelesaikan masalah. Contoh: memasak nasi, menghitung rata-rata nilai. Diagram alir membantu visualisasi.</p>
""", 3),
        ]

    for subject_id, judul, isi, urutan in materials_data:
        if not Material.query.filter_by(subject_id=subject_id, judul=judul).first():
            db.session.add(Material(
                subject_id=subject_id,
                judul=judul,
                isi=isi.strip(),
                urutan=urutan,
                aktif=True,
            ))
    db.session.commit()

    # --- Materi lanjutan berbobot ---
    # Materi lama tidak diubah; judul dipakai sebagai kunci agar seed aman
    # dijalankan berulang kali pada database yang sudah berisi data.
    advanced_materials = [
        (subj["Matematika"].id, "Aljabar: Persamaan Linear Satu Variabel", """
<h3>Memahami Persamaan Linear</h3>
<p>Persamaan linear satu variabel adalah kalimat matematika yang memuat satu peubah berpangkat satu, misalnya <strong>3x + 5 = 20</strong>.</p>
<h4>Langkah penyelesaian</h4>
<ol>
<li>Kurangi 5 dari kedua ruas: 3x = 15.</li>
<li>Bagi kedua ruas dengan 3: x = 5.</li>
</ol>
<p>Operasi yang dilakukan pada satu ruas harus dilakukan juga pada ruas lainnya agar nilai kedua ruas tetap seimbang. Gunakan substitusi untuk memeriksa jawaban.</p>
<p><strong>Latihan:</strong> Tentukan nilai x dari 4x − 7 = 17 dan jelaskan setiap langkahnya.</p>
""", 4),
        (subj["Matematika"].id, "Statistika: Rata-rata, Median, dan Modus", """
<h3>Membaca Data dengan Benar</h3>
<p>Statistika membantu kita mengambil kesimpulan dari sekumpulan data. Rata-rata diperoleh dengan menjumlahkan seluruh data lalu membaginya dengan banyak data.</p>
<ul>
<li><strong>Median:</strong> nilai tengah setelah data diurutkan.</li>
<li><strong>Modus:</strong> nilai yang paling sering muncul.</li>
<li><strong>Jangkauan:</strong> nilai terbesar dikurangi nilai terkecil.</li>
</ul>
<p>Contoh data nilai: 70, 75, 75, 80, 90. Rata-ratanya 78, median 75, dan modus 75. Perhatikan bahwa satu nilai ekstrem dapat memengaruhi rata-rata.</p>
""", 5),
        (subj["Bahasa Indonesia"].id, "Teks Eksplanasi dan Cara Menyusun Argumen", """
<h3>Menjelaskan Proses dan Sebab-Akibat</h3>
<p>Teks eksplanasi menerangkan bagaimana atau mengapa suatu fenomena terjadi. Strukturnya terdiri dari identifikasi fenomena, rangkaian proses/sebab-akibat, dan interpretasi.</p>
<p>Argumen yang baik memiliki pendapat, bukti yang relevan, serta penalaran yang menghubungkan bukti dengan pendapat. Hindari generalisasi berlebihan dan bedakan fakta dari opini.</p>
<p><strong>Tugas:</strong> tulis 3 paragraf tentang proses banjir di lingkungan sekitar. Sertakan minimal dua fakta dan satu usulan solusi.</p>
""", 4),
        (subj["Bahasa Indonesia"].id, "Menulis Esai: Kerangka, Kohesi, dan Revisi", """
<h3>Menulis dengan Gagasan yang Terarah</h3>
<p>Esai yang kuat dimulai dengan tesis yang jelas. Susun kerangka berupa pendahuluan, beberapa paragraf isi, dan penutup yang menguatkan kembali gagasan utama.</p>
<p>Gunakan kata rujukan dan konjungsi agar antarkalimat kohesif. Setelah selesai, revisi isi, struktur, pilihan kata, ejaan, dan tanda baca secara terpisah.</p>
<p><strong>Checklist revisi:</strong> Apakah setiap paragraf memiliki satu ide utama? Apakah bukti mendukung tesis? Apakah kesimpulan menjawab pembahasan?</p>
""", 5),
        (subj["Bahasa Inggris"].id, "Reading Comprehension: Main Idea and Inference", """
<h3>Reading for Meaning</h3>
<p>Untuk memahami bacaan, tentukan <em>main idea</em> setiap paragraf dan tandai kata kunci. <em>Supporting details</em> menjelaskan atau membuktikan gagasan utama.</p>
<p><em>Inference</em> adalah kesimpulan yang ditarik dari informasi tersurat dan konteks. Jangan menambahkan informasi yang tidak didukung teks.</p>
<p><strong>Practice:</strong> read a short article about the Meratus ecosystem, write its main idea, two supporting details, and one reasonable inference.</p>
""", 3),
        (subj["Bahasa Inggris"].id, "Writing: Descriptive and Procedure Text", """
<h3>Writing Clearly in English</h3>
<p>A descriptive text identifies a person, place, or object and describes its characteristics using specific adjectives and the simple present tense.</p>
<p>A procedure text explains how to do something. Use a goal, materials, numbered steps, and command verbs such as <em>prepare</em>, <em>mix</em>, and <em>check</em>.</p>
<p><strong>Task:</strong> write a procedure for making a healthy local snack. Use at least five sequence markers: first, next, then, after that, and finally.</p>
""", 4),
        (subj["IPA"].id, "Ekosistem dan Rantai Makanan", """
<h3>Hubungan Antarorganisme</h3>
<p>Ekosistem terdiri dari komponen biotik dan abiotik yang saling berinteraksi. Energi mengalir dari matahari ke produsen, lalu ke konsumen, dan akhirnya pengurai.</p>
<p>Contoh rantai makanan: matahari → padi → belalang → katak → ular → pengurai. Jika satu populasi berubah drastis, keseimbangan ekosistem dapat terganggu.</p>
<p><strong>Aktivitas:</strong> amati lingkungan sekolah, catat lima komponen biotik dan abiotik, lalu buat satu jaring-jaring makanan.</p>
""", 4),
        (subj["IPA"].id, "Sistem Pernapasan dan Kesehatan", """
<h3>Menjaga Organ Pernapasan</h3>
<p>Udara masuk melalui hidung, melewati faring dan trakea, lalu menuju bronkus dan alveolus. Di alveolus terjadi pertukaran oksigen dan karbon dioksida dengan darah.</p>
<p>Asap rokok, polusi, dan infeksi dapat mengganggu sistem pernapasan. Upaya pencegahan meliputi tidak merokok, memakai masker saat udara buruk, mencuci tangan, dan menjaga ventilasi.</p>
""", 5),
        (subj["IPS"].id, "Interaksi Keruangan dan Perubahan Sosial", """
<h3>Ruang Membentuk Kehidupan Masyarakat</h3>
<p>Interaksi keruangan terjadi ketika manusia, barang, atau informasi berpindah antarruang. Sungai, jalan, pasar, dan teknologi memperkuat hubungan antarwilayah.</p>
<p>Perubahan akses transportasi dan internet dapat membuka peluang ekonomi, tetapi juga memengaruhi pola kerja, budaya, dan lingkungan. Analisis perubahan harus mempertimbangkan manfaat dan risikonya.</p>
<p><strong>Tugas:</strong> bandingkan aktivitas ekonomi di pasar tradisional dan platform digital menggunakan tabel kelebihan serta tantangannya.</p>
""", 4),
        (subj["IPS"].id, "Kegiatan Ekonomi dan Literasi Keuangan", """
<h3>Mengelola Uang dengan Bertanggung Jawab</h3>
<p>Kebutuhan harus diprioritaskan dibanding keinginan. Buat anggaran sederhana dengan mencatat pemasukan, pengeluaran wajib, tabungan, dan dana berbagi.</p>
<p>Kenali risiko penipuan, pinjaman ilegal, dan belanja impulsif. Sebelum membeli, bandingkan harga, kualitas, manfaat, serta kemampuan membayar.</p>
<p><strong>Latihan:</strong> susun anggaran mingguan dari uang saku contoh dan jelaskan alasan pembagian setiap pos.</p>
""", 5),
        (subj["Informatika"].id, "Pemrograman Dasar dengan Python", """
<h3>Variabel, Percabangan, dan Perulangan</h3>
<p>Program memproses data melalui instruksi yang terurut. Variabel menyimpan nilai, percabangan <code>if</code> memilih aksi berdasarkan kondisi, dan perulangan <code>for</code> atau <code>while</code> mengulang aksi.</p>
<pre><code>nilai = 78
if nilai >= 75:
    print("Lulus")
else:
    print("Perlu latihan")</code></pre>
<p>Biasakan memberi nama variabel yang jelas dan menguji program dengan kondisi berbeda.</p>
""", 4),
        (subj["Informatika"].id, "Data, Privasi, dan Etika Digital", """
<h3>Menjadi Warga Digital yang Bertanggung Jawab</h3>
<p>Data pribadi seperti kata sandi, NIK, alamat, dan kode OTP harus dilindungi. Gunakan kata sandi unik, autentikasi dua langkah, dan periksa alamat situs sebelum memasukkan data.</p>
<p>Etika digital berarti menghormati privasi, mencantumkan sumber, tidak menyebarkan hoaks, serta meminta izin sebelum membagikan foto atau karya orang lain.</p>
<p><strong>Studi kasus:</strong> buat langkah pemeriksaan sebelum meneruskan pesan berantai yang mengaku sebagai berita penting.</p>
""", 5),
    ]

    for subject_id, judul, isi, urutan in advanced_materials:
        if not Material.query.filter_by(subject_id=subject_id, judul=judul).first():
            db.session.add(Material(
                subject_id=subject_id,
                judul=judul,
                isi=isi.strip(),
                urutan=urutan,
                aktif=True,
            ))
    db.session.commit()

    if Quiz.query.count() == 0:
        matematika = Subject.query.filter_by(nama="Matematika").first()
        ips = Subject.query.filter_by(nama="IPS").first()
        ipa = Subject.query.filter_by(nama="IPA").first()

        # Quiz Matematika
        quiz_mtk = Quiz(subject_id=matematika.id, judul="Latihan Matematika Dasar", durasi_menit=20)
        db.session.add(quiz_mtk)
        db.session.commit()
        questions_mtk = [
            ("Berapakah 2 + 3?", "4", "5", "6", "7", "B", "2 ditambah 3 sama dengan 5."),
            ("Hasil dari 12 − 7 adalah …", "4", "5", "6", "7", "B", "12 dikurangi 7 = 5."),
            ("6 × 4 = …", "20", "22", "24", "26", "C", "6 kali 4 = 24."),
            ("20 ÷ 5 = …", "2", "3", "4", "5", "C", "20 dibagi 5 = 4."),
            ("25% dari 80 adalah …", "15", "20", "25", "30", "B", "25/100 × 80 = 20."),
        ]
        for p, a, b, c, d, j, bahas in questions_mtk:
            db.session.add(Question(
                quiz_id=quiz_mtk.id,
                pertanyaan=p, opsi_a=a, opsi_b=b, opsi_c=c, opsi_d=d,
                jawaban=j, pembahasan=bahas,
            ))

        # Quiz IPS lokal
        quiz_ips = Quiz(subject_id=ips.id, judul="Kuis Geografi & Budaya Banua", durasi_menit=15)
        db.session.add(quiz_ips)
        db.session.commit()
        questions_ips = [
            ("Ibu kota Kabupaten Hulu Sungai Tengah adalah …", "Banjarmasin", "Barabai", "Martapura", "Kandangan", "B", "Barabai adalah ibu kota Kabupaten HST."),
            ("Barabai sering dijuluki …", "Kota Intan", "Kota Emas", "Kota Batu", "Kota Sungai", "A", "Julukan populer Barabai adalah Kota Intan."),
            ("Pegunungan yang terkenal di Kalimantan Selatan disebut …", "Alps", "Meratus", "Himalaya", "Andes", "B", "Pegunungan Meratus terletak di Kalsel."),
            ("Kain tradisional khas Banjar disebut …", "Batik", "Sasirangan", "Tenun Ikat", "Songket", "B", "Sasirangan adalah kain tradisional Banjar."),
            ("Sungai berperan penting di Kalsel untuk …", "Hanya wisata", "Transportasi & ekonomi", "Hanya irigasi", "Tidak penting", "B", "Sungai mendukung transportasi dan perekonomian."),
        ]
        for p, a, b, c, d, j, bahas in questions_ips:
            db.session.add(Question(
                quiz_id=quiz_ips.id,
                pertanyaan=p, opsi_a=a, opsi_b=b, opsi_c=c, opsi_d=d,
                jawaban=j, pembahasan=bahas,
            ))

        # Quiz IPA
        quiz_ipa = Quiz(subject_id=ipa.id, judul="Latihan IPA: Makhluk Hidup", durasi_menit=15)
        db.session.add(quiz_ipa)
        db.session.commit()
        questions_ipa = [
            ("Salah satu ciri makhluk hidup adalah …", "Tidak bergerak", "Bernapas", "Tidak tumbuh", "Tidak butuh makanan", "B", "Makhluk hidup bernapas, bergerak, tumbuh, dan berkembang biak."),
            ("Energi yang dimiliki benda karena gerak disebut …", "Potensial", "Kinetik", "Kimia", "Nuklir", "B", "Energi kinetik terkait dengan gerak."),
            ("Pusat tata surya kita adalah …", "Bumi", "Bulan", "Matahari", "Mars", "C", "Matahari adalah pusat tata surya."),
        ]
        for p, a, b, c, d, j, bahas in questions_ipa:
            db.session.add(Question(
                quiz_id=quiz_ipa.id,
                pertanyaan=p, opsi_a=a, opsi_b=b, opsi_c=c, opsi_d=d,
                jawaban=j, pembahasan=bahas,
            ))

        db.session.commit()

    # --- Bank soal berbobot per mata pelajaran ---
    # Soal lama dipertahankan. Setiap paket baru dicari berdasarkan judul
    # agar aman dijalankan berulang kali tanpa membuat duplikasi.
    advanced_quizzes = [
        ("Matematika", "Evaluasi Matematika: Aljabar & Statistika", 25, [
            ("Jika 3x + 7 = 25, nilai x adalah ...", "4", "5", "6", "7", "B", "3x = 18 sehingga x = 6."),
            ("Data 6, 8, 8, 10, 13 memiliki median ...", "6", "8", "9", "10", "B", "Data sudah berurutan dan nilai tengahnya adalah 8."),
            ("Sebuah harga Rp120.000 mendapat diskon 15%. Harga setelah diskon adalah ...", "Rp18.000", "Rp102.000", "Rp105.000", "Rp138.000", "B", "Diskon = 15% × 120.000 = 18.000, jadi harga akhir Rp102.000."),
        ]),
        ("Bahasa Indonesia", "Evaluasi Bahasa Indonesia: Teks & Argumen", 25, [
            ("Kalimat yang paling tepat sebagai tesis tentang literasi digital adalah ...", "Literasi digital itu penting.", "Literasi digital membantu siswa menilai informasi secara kritis dan bertanggung jawab.", "Semua orang memakai internet.", "Internet memiliki banyak situs.", "B", "Tesis yang baik spesifik dan memuat gagasan yang dapat didukung argumen."),
            ("Dalam teks eksplanasi, bagian yang menjelaskan urutan proses disebut ...", "Identifikasi fenomena", "Rangkaian kejadian", "Orientasi tokoh", "Koda", "B", "Rangkaian kejadian menjelaskan proses atau hubungan sebab-akibat."),
            ("Bukti paling kuat untuk mendukung pendapat adalah ...", "Kabar dari teman", "Data dan sumber yang dapat diverifikasi", "Komentar anonim", "Perasaan penulis", "B", "Argumen harus didukung bukti yang relevan dan dapat diperiksa."),
        ]),
        ("Bahasa Inggris", "English Assessment: Reading & Writing", 25, [
            ("Choose the correct sentence for a daily habit.", "She study every day.", "She studies every day.", "She studying every day.", "She studied every day yesterday.", "B", "For third-person singular in the simple present, study becomes studies."),
            ("The main purpose of a procedure text is to ...", "describe a person", "explain how to do or make something", "tell a past story", "argue about an issue", "B", "A procedure text presents a goal, materials, and ordered steps."),
            ("If a text says the river is clean because residents work together, we can infer that ...", "the river has no fish", "community cooperation supports environmental care", "residents avoid the river", "the river is dangerous", "B", "The stated cause supports the inference about collective environmental action."),
        ]),
        ("IPA", "Evaluasi IPA: Ekosistem & Kesehatan", 25, [
            ("Jika jumlah ular di sawah menurun drastis, kemungkinan awal yang terjadi adalah ...", "populasi tikus meningkat", "padi berhenti tumbuh", "matahari berkurang", "pengurai menghilang", "A", "Ular memangsa tikus, sehingga penurunan predator dapat meningkatkan populasi mangsa."),
            ("Pertukaran oksigen dan karbon dioksida pada manusia terjadi terutama di ...", "trakea", "bronkus", "alveolus", "rongga hidung", "C", "Alveolus berdinding tipis dan dikelilingi kapiler untuk pertukaran gas."),
            ("Energi potensial gravitasi benda bertambah ketika ...", "massanya dan ketinggiannya bertambah", "warnanya berubah", "suhunya selalu turun", "kecepatannya menjadi nol", "A", "Energi potensial gravitasi dipengaruhi massa, gravitasi, dan ketinggian."),
        ]),
        ("IPS", "Evaluasi IPS: Ruang, Ekonomi & Banua", 25, [
            ("Perubahan akses jalan dan internet terhadap kegiatan ekonomi menunjukkan adanya ...", "isolasi ruang", "interaksi keruangan", "perubahan cuaca", "siklus hidrologi", "B", "Perpindahan orang, barang, dan informasi antarwilayah adalah interaksi keruangan."),
            ("Contoh perilaku literasi keuangan yang tepat adalah ...", "membeli tanpa membandingkan harga", "mencatat pengeluaran dan memprioritaskan kebutuhan", "membagikan kode OTP", "meminjam dari sumber tidak resmi", "B", "Pencatatan dan prioritas membantu mengelola uang secara sadar."),
            ("Sasirangan penting dipelajari sebagai bagian dari ...", "budaya dan identitas masyarakat Banjar", "iklim Kalimantan", "sistem tata surya", "teknologi komunikasi", "A", "Sasirangan merupakan warisan budaya yang memperkuat identitas Banjar."),
        ]),
        ("Informatika", "Evaluasi Informatika: Algoritma & Keamanan", 25, [
            ("Struktur yang digunakan untuk memilih aksi berdasarkan kondisi adalah ...", "variabel", "percabangan", "komentar", "input perangkat", "B", "Percabangan seperti if memilih instruksi berdasarkan kondisi benar atau salah."),
            ("Kata sandi yang paling aman adalah ...", "12345678", "nama dan tanggal lahir", "kombinasi unik panjang dengan autentikasi dua langkah", "satu kata yang dipakai di semua akun", "C", "Kata sandi unik dan 2FA mengurangi risiko pengambilalihan akun."),
            ("Langkah pertama yang paling tepat saat menerima berita berantai adalah ...", "langsung meneruskan", "memeriksa sumber dan membandingkan dengan rujukan tepercaya", "menghapus semua aplikasi", "mengubah judul berita", "B", "Verifikasi sumber dan pembanding membantu mencegah penyebaran hoaks."),
        ]),
    ]

    for subject_name, quiz_title, duration, question_data in advanced_quizzes:
        subject = subj[subject_name]
        quiz = Quiz.query.filter_by(subject_id=subject.id, judul=quiz_title).first()
        if not quiz:
            quiz = Quiz(
                subject_id=subject.id,
                judul=quiz_title,
                durasi_menit=duration,
                aktif=True,
            )
            db.session.add(quiz)
            db.session.flush()

        for question_data_item in question_data:
            question_text = question_data_item[0]
            if not Question.query.filter_by(
                quiz_id=quiz.id,
                pertanyaan=question_text,
            ).first():
                p, a, b, c, d, answer, explanation = question_data_item
                db.session.add(Question(
                    quiz_id=quiz.id,
                    pertanyaan=p,
                    opsi_a=a,
                    opsi_b=b,
                    opsi_c=c,
                    opsi_d=d,
                    jawaban=answer,
                    pembahasan=explanation,
                ))

    # Lengkapi semua ujian aktif menjadi 30 soal. Bank ringkas ini dipakai
    # untuk ujian lama maupun paket baru yang sudah memiliki tiga soal awal.
    # Soal lama tetap dipertahankan dan soal tambahan memiliki pembahasan.
    question_pools = {
        "Matematika": [
            ("Jika 5x - 10 = 25, nilai x adalah ...", "5", "6", "7", "8", "B", "5x = 35 sehingga x = 7."),
            ("Luas persegi panjang dengan panjang 12 cm dan lebar 5 cm adalah ...", "17 cm2", "34 cm2", "60 cm2", "120 cm2", "C", "Luas = panjang × lebar = 12 × 5 = 60 cm2."),
            ("Peluang muncul sisi gambar pada sebuah koin seimbang adalah ...", "0", "1/4", "1/2", "1", "C", "Ada satu hasil yang diinginkan dari dua hasil yang sama mungkin."),
            ("Bentuk desimal dari 3/4 adalah ...", "0,25", "0,5", "0,75", "1,25", "C", "3 dibagi 4 sama dengan 0,75."),
            ("Jika 2 : 5 = x : 20, nilai x adalah ...", "4", "8", "10", "12", "B", "2/5 = x/20, sehingga x = 8."),
            ("Sudut siku-siku besarnya ...", "45°", "90°", "180°", "360°", "B", "Sudut siku-siku memiliki ukuran 90 derajat."),
            ("KPK dari 6 dan 8 adalah ...", "12", "18", "24", "48", "C", "Kelipatan terkecil yang sama adalah 24."),
            ("Jika 20% dari suatu bilangan adalah 16, bilangan itu ...", "32", "64", "80", "96", "C", "0,2n = 16, maka n = 80."),
            ("Pola 3, 6, 12, 24, ... dilanjutkan dengan ...", "30", "36", "48", "60", "C", "Setiap suku dikali 2, sehingga 24 × 2 = 48."),
        ],
        "Bahasa Indonesia": [
            ("Gagasan utama biasanya menjadi dasar pengembangan ...", "judul saja", "kalimat penjelas", "tanda baca", "daftar pustaka", "B", "Kalimat penjelas menguraikan gagasan utama."),
            ("Kata baku yang tepat adalah ...", "resiko", "ijin", "aktivitas", "praktek", "C", "Bentuk baku yang benar adalah aktivitas."),
            ("Kalimat efektif harus mengutamakan ...", "kerancuan", "kehematan dan kejelasan", "pengulangan", "kata asing", "B", "Kalimat efektif jelas, hemat, logis, dan sesuai kaidah."),
            ("Majas yang membandingkan dua hal secara langsung disebut ...", "metafora", "ironi", "repetisi", "litotes", "A", "Metafora membandingkan tanpa kata pembanding seperti."),
            ("Tujuan simpulan dalam teks adalah ...", "memperkenalkan tokoh", "merangkum gagasan penting", "menambah konflik", "mengubah topik", "B", "Simpulan merangkum inti pembahasan."),
            ("Informasi yang dapat dibuktikan kebenarannya disebut ...", "opini", "fakta", "saran", "prediksi", "B", "Fakta memiliki dasar atau bukti yang dapat diverifikasi."),
            ("Kata hubung yang menyatakan sebab adalah ...", "tetapi", "karena", "kemudian", "atau", "B", "Karena menghubungkan sebab dengan akibat."),
            ("Struktur awal teks prosedur biasanya berisi ...", "tujuan", "konflik", "koda", "argumentasi", "A", "Tujuan menjelaskan hasil yang hendak dicapai."),
            ("Paragraf yang ide utamanya berada di akhir disebut paragraf ...", "deduktif", "induktif", "naratif", "deskriptif", "B", "Paragraf induktif menyajikan rincian sebelum simpulan utama."),
        ],
        "Bahasa Inggris": [
            ("The past form of 'go' is ...", "goed", "gone", "went", "going", "C", "The irregular past form of go is went."),
            ("Choose the correct article: She bought ... umbrella.", "a", "an", "the a", "some an", "B", "Umbrella begins with a vowel sound, so use an."),
            ("The opposite of 'difficult' is ...", "easy", "slow", "late", "heavy", "A", "Easy means not difficult."),
            ("'They are studying' is in the ... tense.", "simple past", "present continuous", "simple future", "present perfect", "B", "The be verb plus -ing marks present continuous."),
            ("A word that describes a noun is called an ...", "adverb", "adjective", "article", "pronoun", "B", "An adjective describes a noun."),
            ("The correct question for 'I live in Barabai' is ...", "Where do you live?", "Where are you live?", "Where did you lives?", "Where living you?", "A", "Use do with you and the base verb live."),
            ("'Because' is used to introduce a ...", "reason", "contrast", "place", "question", "A", "Because introduces a reason."),
            ("The plural form of 'child' is ...", "childs", "childes", "children", "childrens", "C", "Children is the irregular plural form."),
            ("A procedure should present steps in ... order.", "random", "logical", "silent", "reverse only", "B", "Logical order makes instructions easy to follow."),
        ],
        "IPA": [
            ("Organisms that make their own food are called ...", "consumers", "producers", "decomposers", "predators", "B", "Plants are producers because they make food by photosynthesis."),
            ("The change from liquid to gas is called ...", "freezing", "melting", "evaporation", "condensation", "C", "Evaporation changes a liquid into gas."),
            ("The force that pulls objects toward Earth is ...", "friction", "gravity", "magnetism", "buoyancy", "B", "Gravity attracts objects toward Earth."),
            ("The organ that pumps blood is the ...", "lung", "heart", "kidney", "stomach", "B", "The heart pumps blood throughout the body."),
            ("Plants release oxygen mainly through ...", "photosynthesis", "digestion", "respiration only", "filtration", "A", "Photosynthesis produces oxygen as a by-product."),
            ("A material that does not allow electricity to pass easily is an ...", "conductor", "insulator", "electrolyte", "magnet", "B", "Insulators resist the flow of electric current."),
            ("The Earth completes one rotation in about ...", "12 hours", "24 hours", "30 days", "365 days", "B", "Rotation causes day and night and takes about 24 hours."),
            ("Sound needs ... to travel.", "a medium", "absolute darkness", "only sunlight", "a vacuum", "A", "Sound is a mechanical wave and needs a medium."),
            ("The first level in most food chains is occupied by ...", "producers", "secondary consumers", "decomposers only", "scavengers", "A", "Energy enters the food chain through producers."),
        ],
        "IPS": [
            ("Kegiatan menghasilkan barang atau jasa disebut ...", "konsumsi", "produksi", "distribusi", "transaksi", "B", "Produksi menghasilkan barang atau jasa."),
            ("Pihak yang menyalurkan barang dari produsen ke konsumen disebut ...", "distributor", "investor", "konsumen", "regulator", "A", "Distributor menyalurkan barang dalam rantai ekonomi."),
            ("Peta digunakan terutama untuk menunjukkan ...", "letak dan kondisi wilayah", "rasa makanan", "jumlah suara", "sifat tokoh", "A", "Peta menyajikan informasi keruangan."),
            ("Contoh sumber daya alam yang dapat diperbarui adalah ...", "minyak bumi", "batu bara", "sinar matahari", "gas alam", "C", "Sinar matahari tersedia secara berkelanjutan."),
            ("Musyawarah mencerminkan nilai ...", "demokrasi", "persaingan bebas", "isolasi", "individualisme", "A", "Musyawarah memberi ruang untuk keputusan bersama."),
            ("Keragaman budaya sebaiknya dihadapi dengan sikap ...", "merendahkan", "toleransi", "memaksa", "menutup diri", "B", "Toleransi menghargai perbedaan."),
            ("Inflasi berarti kecenderungan ...", "harga umum naik", "produksi selalu turun", "uang tidak berlaku", "pajak hilang", "A", "Inflasi adalah kenaikan harga umum secara berkelanjutan."),
            ("Pasar mempertemukan ...", "penjual dan pembeli", "guru dan siswa saja", "pemerintah dan hakim", "dokter dan pasien saja", "A", "Pasar menjadi tempat interaksi penjual dan pembeli."),
            ("Gotong royong menunjukkan pentingnya ...", "kerja sama", "perselisihan", "ketergantungan pasif", "persaingan", "A", "Gotong royong adalah kerja sama untuk tujuan bersama."),
        ],
        "Informatika": [
            ("Data yang telah diolah sehingga bermakna disebut ...", "informasi", "perangkat keras", "sinyal", "kode sumber", "A", "Informasi adalah data yang telah diproses dan memiliki makna."),
            ("Langkah terurut untuk menyelesaikan masalah disebut ...", "algoritma", "folder", "browser", "piksel", "A", "Algoritma berisi langkah penyelesaian yang terstruktur."),
            ("Perangkat untuk memasukkan teks ke komputer adalah ...", "monitor", "keyboard", "speaker", "proyektor", "B", "Keyboard merupakan perangkat input untuk teks."),
            ("Salinan data untuk mengantisipasi kehilangan disebut ...", "backup", "spam", "cache", "kompresi", "A", "Backup adalah salinan cadangan data."),
            ("Jaringan global yang menghubungkan banyak perangkat disebut ...", "internet", "printer", "database lokal", "clipboard", "A", "Internet menghubungkan jaringan dan perangkat di seluruh dunia."),
            ("Dalam Python, tanda untuk komentar satu baris adalah ...", "//", "#", "<!--", "**", "B", "Python memakai # untuk komentar satu baris."),
            ("Phishing biasanya bertujuan mencuri ...", "data pribadi", "warna layar", "ukuran file", "kecepatan CPU", "A", "Phishing menipu pengguna agar memberikan data sensitif."),
            ("Perulangan digunakan untuk ...", "mengulang instruksi", "menghapus listrik", "menggambar monitor", "mengubah keyboard", "A", "Loop menjalankan instruksi berulang berdasarkan kondisi."),
            ("Sumber informasi yang paling layak dipercaya adalah ...", "situs resmi dan sumber yang dapat diverifikasi", "pesan anonim", "judul tanpa tautan", "komentar acak", "A", "Sumber tepercaya memiliki identitas dan bukti yang bisa diperiksa."),
        ],
    }

    for quiz in Quiz.query.filter_by(aktif=True).all():
        pool = question_pools.get(quiz.subject.nama)
        if not pool:
            continue
        existing = Question.query.filter_by(quiz_id=quiz.id).count()
        for index in range(existing, 30):
            p, a, b, c, d, answer, explanation = pool[index % len(pool)]
            db.session.add(Question(
                quiz_id=quiz.id,
                pertanyaan=f"{p} (Latihan pengayaan {index + 1})",
                opsi_a=a,
                opsi_b=b,
                opsi_c=c,
                opsi_d=d,
                jawaban=answer,
                pembahasan=explanation,
            ))
    db.session.commit()

print("Seed selesai.")
print("Admin: username=admin, password=admin123")
print("Segera ganti password admin setelah login.")
print("Materi & ujian (termasuk konten lokal Barabai/Kalsel) telah diisi.")
