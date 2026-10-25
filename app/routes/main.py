from flask import Blueprint, render_template, Response, url_for
from app.models import Project

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template('index.html')


@main_bp.route('/about')
def about():
    about_stats = [
        {"label": "Proyek dikerjakan", "value": 0, "suffix": "+"},
        {"label": "Teknologi yang dikuasai", "value": 0, "suffix": "+"},
        {"label": "Tahun belajar coding", "value": 0, "suffix": ""},
    ]
    return render_template('about.html', about_stats=about_stats)

@main_bp.route("/skills")
def skills():
    skill_categories = [
        {
            "category": "Programming Languages",
            "skills": [
                {"name": "Python", "level": "Currently Learning"},
                {"name": "PHP", "level": "Currently Learning"},
                {"name": "JavaScript", "level": "Currently Learning"},
                {"name": "TypeScript", "level": "Currently Learning"},
                {"name": "Dart", "level": "Currently Learning"},
                {"name": "C++", "level": "Currently Learning"},
                {"name": "SQL", "level": "Currently Learning"},
            ],
        },
        {
            "category": "Backend & Framework",
            "skills": [
                {"name": "Flask", "level": "Currently Learning"},
                {"name": "Laravel", "level": "Currently Learning"},
                {"name": "REST API", "level": "Currently Learning"},
                {"name": "Authentication", "level": "Currently Learning"},
                {"name": "Database Management", "level": "Currently Learning"},
            ],
        },
        {
            "category": "Frontend",
            "skills": [
                {"name": "HTML", "level": "Currently Learning"},
                {"name": "CSS", "level": "Currently Learning"},
                {"name": "Tailwind CSS", "level": "Currently Learning"},
                {"name": "Bootstrap", "level": "Currently Learning"},
                {"name": "React / Next.js (dasar)", "level": "Currently Learning"},
            ],
        },
        {
            "category": "Mobile Development",
            "skills": [
                {"name": "Flutter", "level": "Currently Learning"},
                {"name": "REST API Integration", "level": "Currently Learning"},
                {"name": "Shared Preferences", "level": "Currently Learning"},
            ],
        },
        {
            "category": "Database & Tools",
            "skills": [
                {"name": "MySQL", "level": "Currently Learning"},
                {"name": "SQLite", "level": "Currently Learning"},
                {"name": "Git", "level": "Currently Learning"},
                {"name": "GitHub", "level": "Currently Learning"},
                {"name": "Postman", "level": "Currently Learning"},
                {"name": "Visual Studio Code", "level": "Currently Learning"},
                {"name": "Figma", "level": "Currently Learning"},
            ],
        },
    ]
    return render_template("skills.html", skill_categories=skill_categories)

@main_bp.route("/journey")
def journey():
    milestones = [
        {
            "period": "2023 - 2026",
            "title": "SMKN 1 Sumedang - Rekayasa Perangkat Lunak",
            "description": "Mulai belajar dasar-dasar pemrograman dan pengembangan perangkat lunak.",
        },
        {
            "period": "2023 - 2024",
            "title": "Mulai Belajar Web Development",
            "description": "Mempelajari dasar HTML, CSS, dan JavaScript untuk membangun website.",
        },
        {
            "period": "2025 - 2026",
            "title": "Membuat Proyek dengan Laravel",
            "description": "Mulai membangun proyek web menggunakan Laravel, termasuk Readify dan SmartFit.",
        },
        {
            "period": "2024 - 2025",
            "title": "Mempelajari Flutter",
            "description": "Memperluas kemampuan ke pengembangan aplikasi mobile dengan Flutter.",
        },
        {
            "period": "2025 - 2026",
            "title": "Membuat Proyek Aplikasi Mobile",
            "description": "Mengembangkan aplikasi mobile, termasuk Personal Finance App.",
        },
        {
            "period": "2026 - Sekarang",
            "title": "Universitas Siliwangi - Informatika",
            "description": "Melanjutkan studi Informatika untuk memperdalam ilmu di bidang software engineering.",
        },
        {
            "period": "Sekarang",
            "title": "Mendalami Backend, API & Database",
            "description": "Fokus memperdalam backend development, API, dan database management.",
        },
        {
            "period": "Target",
            "title": "Menjadi Backend Developer / Software Developer",
            "description": "Terus belajar dan membangun portofolio menuju karier sebagai Software Developer.",
        },
    ]
    return render_template("journey.html", milestones=milestones)

@main_bp.route("/robots.txt")
def robots():
    content = (
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /admin/\n"
        f"Sitemap: {url_for('main.sitemap', _external=True)}\n"
    )
    return Response(content, mimetype="text/plain")


@main_bp.route("/sitemap.xml")
def sitemap():
    pages = [
        url_for("main.home", _external=True),
        url_for("main.about", _external=True),
        url_for("main.skills", _external=True),
        url_for("projects.project_list", _external=True),
        url_for("main.journey", _external=True),
        url_for("contact.contact", _external=True),
    ]

    for project in Project.query.all():
        pages.append(url_for("projects.project_detail", slug=project.slug, _external=True))

    xml_items = "\n".join(f"  <url><loc>{page}</loc></url>" for page in pages)
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{xml_items}\n"
        "</urlset>"
    )

    return Response(xml, mimetype="application/xml")