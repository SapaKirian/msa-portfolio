from datetime import datetime
from flask import Flask, render_template
from config import Config
from app.extensions import db, csrf, login_manager, compress


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    @app.context_processor
    def inject_current_year():
        return {"current_year": datetime.utcnow().year}

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404

    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    compress.init_app(app)
    login_manager.login_view = "admin.login"
    login_manager.login_message = "Silakan login terlebih dahulu."
    login_manager.login_message_category = "warning"

    @login_manager.user_loader
    def load_user(user_id):
        from app.models import Admin
        return Admin.query.get(int(user_id))

    from app.routes.main import main_bp
    app.register_blueprint(main_bp)

    from app.routes.projects import projects_bp
    app.register_blueprint(projects_bp)

    from app.routes.contact import contact_bp
    app.register_blueprint(contact_bp)

    from app.routes.admin import admin_bp
    app.register_blueprint(admin_bp)

    with app.app_context():
        from app import models
        db.create_all()

    @app.cli.command("create-admin")
    def create_admin():
        """Buat akun admin baru lewat terminal."""
        import getpass
        from app.models import Admin

        username = input("Username admin: ")
        password = getpass.getpass("Password admin: ")

        if Admin.query.filter_by(username=username).first():
            print("Username sudah dipakai, coba username lain.")
            return

        admin = Admin(username=username)
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
        print(f"Admin '{username}' berhasil dibuat.")

    @app.cli.command("seed-projects")
    def seed_projects():
        """Isi data proyek awal ke database (hanya sekali, aman dijalankan ulang)."""
        from app.models import Project

        seed_data = [
            {
                "title": "Readify",
                "slug": "readify",
                "category": "Web Development",
                "short_description": "Platform perpustakaan digital dengan katalog, pencarian, dan sistem peminjaman buku.",
                "technologies": "Laravel, MySQL, Blade, Bootstrap",
                "status": "Completed",
                "role": "TODO: tulis peranmu di proyek ini",
                "problem": "TODO: jelaskan masalah yang ingin diselesaikan proyek ini",
                "solution": "TODO: jelaskan solusi yang kamu kembangkan",
                "features": "Katalog buku\nKategori\nPencarian\nPeminjaman\nFavorit\nRiwayat\nProfil pengguna",
                "challenges": "TODO: ceritakan tantangan teknis yang kamu hadapi",
                "results": "TODO: ceritakan hasil dan pembelajaran dari proyek ini",
                "thumbnail": "readify.jpg",
            },
            {
                "title": "SmartFit",
                "slug": "smartfit",
                "category": "Web Development",
                "short_description": "E-commerce seragam SMA, mulai dari katalog produk sampai checkout dan pickup di toko.",
                "technologies": "Laravel, MySQL, Blade, JavaScript",
                "status": "Completed",
                "role": "TODO: tulis peranmu di proyek ini",
                "problem": "TODO: jelaskan masalah yang ingin diselesaikan proyek ini",
                "solution": "TODO: jelaskan solusi yang kamu kembangkan",
                "features": "Daftar produk\nDetail produk\nKeranjang\nCheckout\nPembayaran\nPickup di toko\nProfil\nRiwayat pesanan",
                "challenges": "TODO: ceritakan tantangan teknis yang kamu hadapi",
                "results": "TODO: ceritakan hasil dan pembelajaran dari proyek ini",
                "thumbnail": "smartfit.jpg",
            },
            {
                "title": "JPM Yamaha",
                "slug": "jpm-yamaha",
                "category": "Web Development",
                "short_description": "Platform promosi dan layanan dealer Yamaha, dilengkapi dashboard admin dan aplikasi mobile.",
                "technologies": "Laravel, Filament, Flutter, MySQL, REST API",
                "status": "Completed",
                "role": "TODO: tulis peranmu di proyek ini",
                "problem": "TODO: jelaskan masalah yang ingin diselesaikan proyek ini",
                "solution": "TODO: jelaskan solusi yang kamu kembangkan",
                "features": "Katalog motor\nPromo\nBerita\nJadwal bengkel\nFAQ\nAplikasi mobile\nDashboard admin",
                "challenges": "TODO: ceritakan tantangan teknis yang kamu hadapi",
                "results": "TODO: ceritakan hasil dan pembelajaran dari proyek ini",
                "thumbnail": "jpm-yamaha.jpg",
            },
            {
                "title": "Personal Finance App",
                "slug": "personal-finance-app",
                "category": "Mobile Development",
                "short_description": "Aplikasi mobile untuk mencatat pemasukan, pengeluaran, dan melihat ringkasan laporan keuangan.",
                "technologies": "Flutter, REST API, SQLite",
                "status": "Completed",
                "role": "TODO: tulis peranmu di proyek ini",
                "problem": "TODO: jelaskan masalah yang ingin diselesaikan proyek ini",
                "solution": "TODO: jelaskan solusi yang kamu kembangkan",
                "features": "Mencatat pemasukan\nMencatat pengeluaran\nMembuat kategori transaksi\nMenampilkan ringkasan\nMelihat laporan keuangan",
                "challenges": "TODO: ceritakan tantangan teknis yang kamu hadapi",
                "results": "TODO: ceritakan hasil dan pembelajaran dari proyek ini",
                "thumbnail": "personal-finance-app.jpg",
            },
        ]

        added = 0
        for data in seed_data:
            if not Project.query.filter_by(slug=data["slug"]).first():
                db.session.add(Project(**data))
                added += 1

        db.session.commit()
        print(f"{added} proyek baru ditambahkan ke database.")

    return app