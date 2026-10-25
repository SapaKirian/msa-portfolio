# MSA Portfolio — F1 Digital Racing Portfolio

Website portofolio pribadi Muhammad Syava Argiean (MSA), dibangun dengan Python & Flask, bertema *Formula 1 Digital Racing Portfolio*. Dibuat sambil belajar backend development, Flask, dan database management.

## ✨ Fitur

- Loading screen dengan progress bar, lampu start F1, dan indikator RPM
- Navbar sticky dengan efek blur saat scroll, hamburger menu di mobile
- Hero section dengan animasi GSAP dan elemen visual (grid, speed lines)
- Halaman About dengan statistik animatif (count-up)
- Halaman Skills dengan efek tilt 3D pada kartu
- Halaman Projects dengan filter kategori dan halaman detail per proyek
- Halaman Journey dengan timeline animasi (GSAP ScrollTrigger)
- Formulir kontak (Flask-WTF, validasi server-side, CSRF, honeypot, submit via AJAX)
- Dashboard admin: login (Flask-Login), CRUD proyek dengan upload thumbnail, kelola pesan masuk
- Halaman 404 bertema F1
- SEO dasar (meta tags, Open Graph, Twitter Card, sitemap.xml, robots.txt)
- Lazy loading gambar dan kompresi aset (Flask-Compress)
- Responsif di HP, tablet, laptop, dan desktop

## 🛠️ Teknologi

**Backend:** Python 3, Flask, Flask-SQLAlchemy, Flask-WTF, Flask-Login, python-dotenv, Flask-Compress, SQLite

**Frontend:** HTML5, CSS3, JavaScript, GSAP + ScrollTrigger, Font Awesome, Google Fonts

## 📁 Struktur Folder

```
portfolio-python/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── forms.py
│   ├── extensions.py
│   ├── routes/
│   │   ├── main.py
│   │   ├── projects.py
│   │   ├── contact.py
│   │   └── admin.py
│   ├── templates/
│   └── static/
│       ├── css/
│       ├── js/
│       └── images/
├── instance/            (dibuat otomatis, tidak masuk Git)
├── config.py
├── run.py
├── requirements.txt
├── .env                 (tidak masuk Git)
├── .env.example
└── .gitignore
```

## 🖥️ Persyaratan Sistem

- Python 3.10 atau lebih baru
- pip
- Git

## 🚀 Instalasi & Menjalankan Proyek

### 1. Clone repository

```
git clone https://github.com/username-mu/nama-repo.git
cd nama-repo
```

### 2. Buat virtual environment

```
python -m venv venv
```

### 3. Aktifkan virtual environment

Windows (PowerShell):
```
venv\Scripts\Activate.ps1
```

macOS/Linux:
```
source venv/bin/activate
```

### 4. Install dependency

```
pip install -r requirements.txt
```

### 5. Buat file `.env`

Salin `.env.example` jadi `.env`, lalu isi `SECRET_KEY` dengan teks acak rahasia:

```
SECRET_KEY=ganti-dengan-teks-acak-rahasia-punyamu
```

### 6. Jalankan aplikasi (ini juga yang membuat database & tabelnya)

```
python run.py
```

Database (`instance/portfolio.db`) dan semua tabelnya dibuat otomatis saat pertama kali dijalankan.

### 7. Buat akun admin

```
flask --app run.py create-admin
```

### 8. (Opsional) Isi data proyek awal

```
flask --app run.py seed-projects
```

Buka `http://127.0.0.1:5000` di browser.

## 🔑 Login Admin

Buka `http://127.0.0.1:5000/admin/login`, gunakan username/password yang dibuat di langkah instalasi.

## 🎨 Mengganti Identitas

- **Hero (Home):** `app/templates/index.html`
- **Cerita About & statistik:** `app/routes/main.py`, fungsi `about()`
- **Daftar skill:** `app/routes/main.py`, fungsi `skills()`
- **Timeline Journey:** `app/routes/main.py`, fungsi `journey()`
- **Footer:** `app/templates/components/footer.html`
- **Identitas JSON-LD (SEO):** `app/templates/base.html`

## 🖼️ Mengganti Foto Profil

Taruh file foto di `app/static/images/profile/profile.jpg` (nama dan lokasi harus persis sama).

## 📄 Mengganti CV

1. Taruh file PDF CV di `app/static/documents/cv.pdf`.
2. Update link tombol "Download CV" di `app/templates/components/navbar.html` dan `app/templates/index.html` supaya mengarah ke `{{ url_for('static', filename='documents/cv.pdf') }}`.

## ➕ Menambahkan Proyek Baru

Login ke dashboard admin → menu **Projects** → tombol **"+ Tambah Proyek"**. Proyek baru otomatis muncul di halaman publik dan sitemap.

## 🧪 Testing

Proyek ini belum punya automated test suite — pengujian sejauh ini dilakukan manual lewat browser di tiap tahap pengembangan. Ke depannya disarankan menambahkan `pytest` untuk menguji route dan model secara otomatis.

## 🌐 Deployment

Bagian ini akan dilengkapi di tahap berikutnya.

## 📝 Catatan: Hal yang Masih Perlu Diisi

Beberapa bagian masih berisi placeholder `TODO`, silakan diisi sebelum publish:

- Email, lokasi, dan status ketersediaan (`app/templates/contact.html`, `footer.html`)
- Link GitHub/LinkedIn/Instagram (hero dan footer)
- File CV (lihat bagian "Mengganti CV" di atas)
- Foto profil (lihat bagian "Mengganti Foto Profil")
- Angka statistik di halaman About (`app/routes/main.py`, fungsi `about()`)
- Level skill yang sebenarnya (`app/routes/main.py`, fungsi `skills()`)
- Periode/tahun di timeline Journey (`app/routes/main.py`, fungsi `journey()`)
- Cerita tiap proyek: peran, masalah, solusi, tantangan, hasil (lewat dashboard admin, menu Edit proyek)
- Thumbnail dan galeri screenshot proyek asli (lewat dashboard admin)