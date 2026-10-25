from flask import Blueprint, render_template, abort
from app.models import Project

projects_bp = Blueprint("projects", __name__)


@projects_bp.route("/projects")
def project_list():
    categories = ["All", "Web Development", "Mobile Development", "Backend", "UI/UX"]
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template("projects.html", projects=projects, categories=categories)


@projects_bp.route("/projects/<slug>")
def project_detail(slug):
    project = Project.query.filter_by(slug=slug).first()

    if project is None:
        abort(404)

    all_projects = Project.query.order_by(Project.created_at.asc()).all()
    index = all_projects.index(project)
    prev_project = all_projects[index - 1] if index > 0 else None
    next_project = all_projects[index + 1] if index < len(all_projects) - 1 else None

    return render_template(
        "project_detail.html",
        project=project,
        prev_project=prev_project,
        next_project=next_project,
    )