import os
from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from app.forms import LoginForm, ProjectForm
from app.extensions import db
from app.models import Admin, Project, ContactMessage

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def save_thumbnail(file_storage, slug):
    filename = secure_filename(f"{slug}-{file_storage.filename}")
    filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    file_storage.save(filepath)
    return filename


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("admin.dashboard"))

    form = LoginForm()

    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first()

        if admin and admin.check_password(form.password.data):
            login_user(admin)
            flash("Login berhasil!", "success")
            return redirect(url_for("admin.dashboard"))

        flash("Username atau password salah.", "error")

    return render_template("admin/login.html", form=form)


@admin_bp.route("/dashboard")
@login_required
def dashboard():
    stats = {
        "total_projects": Project.query.count(),
        "featured_projects": Project.query.filter_by(featured=True).count(),
        "unread_messages": ContactMessage.query.filter_by(is_read=False).count(),
        "total_messages": ContactMessage.query.count(),
    }
    return render_template("admin/dashboard.html", stats=stats)


@admin_bp.route("/projects")
@login_required
def projects():
    all_projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template("admin/projects.html", projects=all_projects)


@admin_bp.route("/projects/new", methods=["GET", "POST"])
@login_required
def new_project():
    form = ProjectForm()

    if form.validate_on_submit():
        if Project.query.filter_by(slug=form.slug.data).first():
            flash("Slug sudah dipakai proyek lain, gunakan slug yang berbeda.", "error")
            return render_template("admin/project_form.html", form=form, mode="new")

        project = Project(
            title=form.title.data,
            slug=form.slug.data,
            category=form.category.data,
            short_description=form.short_description.data,
            role=form.role.data,
            problem=form.problem.data,
            solution=form.solution.data,
            challenges=form.challenges.data,
            results=form.results.data,
            technologies=form.technologies.data,
            features=form.features.data,
            demo_url=form.demo_url.data or None,
            repo_url=form.repo_url.data or None,
            status=form.status.data,
            year=form.year.data,
            featured=form.featured.data,
        )

        if form.thumbnail.data:
            project.thumbnail = save_thumbnail(form.thumbnail.data, form.slug.data)

        db.session.add(project)
        db.session.commit()

        flash(f'Proyek "{project.title}" berhasil ditambahkan.', "success")
        return redirect(url_for("admin.projects"))

    return render_template("admin/project_form.html", form=form, mode="new")


@admin_bp.route("/projects/<int:project_id>/edit", methods=["GET", "POST"])
@login_required
def edit_project(project_id):
    project = Project.query.get_or_404(project_id)
    form = ProjectForm(obj=project)

    if form.validate_on_submit():
        existing = Project.query.filter_by(slug=form.slug.data).first()
        if existing and existing.id != project.id:
            flash("Slug sudah dipakai proyek lain, gunakan slug yang berbeda.", "error")
            return render_template("admin/project_form.html", form=form, mode="edit", project=project)

        project.title = form.title.data
        project.slug = form.slug.data
        project.category = form.category.data
        project.short_description = form.short_description.data
        project.role = form.role.data
        project.problem = form.problem.data
        project.solution = form.solution.data
        project.challenges = form.challenges.data
        project.results = form.results.data
        project.technologies = form.technologies.data
        project.features = form.features.data
        project.demo_url = form.demo_url.data or None
        project.repo_url = form.repo_url.data or None
        project.status = form.status.data
        project.year = form.year.data
        project.featured = form.featured.data

        if form.thumbnail.data:
            project.thumbnail = save_thumbnail(form.thumbnail.data, form.slug.data)

        db.session.commit()

        flash(f'Proyek "{project.title}" berhasil diperbarui.', "success")
        return redirect(url_for("admin.projects"))

    return render_template("admin/project_form.html", form=form, mode="edit", project=project)


@admin_bp.route("/projects/<int:project_id>/delete", methods=["POST"])
@login_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    flash(f'Proyek "{project.title}" berhasil dihapus.', "success")
    return redirect(url_for("admin.projects"))

@admin_bp.route("/messages")
@login_required
def messages():
    all_messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return render_template("admin/messages.html", messages=all_messages)


@admin_bp.route("/messages/<int:message_id>")
@login_required
def message_detail(message_id):
    message = ContactMessage.query.get_or_404(message_id)

    if not message.is_read:
        message.is_read = True
        db.session.commit()

    return render_template("admin/message_detail.html", message=message)

@admin_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Kamu sudah logout.", "success")
    return redirect(url_for("admin.login"))