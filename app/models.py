from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db


class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ContactMessage {self.id} dari {self.name}>"


class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<Admin {self.username}>"


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    slug = db.Column(db.String(150), unique=True, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    short_description = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(150))
    problem = db.Column(db.Text)
    solution = db.Column(db.Text)
    challenges = db.Column(db.Text)
    results = db.Column(db.Text)
    technologies = db.Column(db.Text)
    features = db.Column(db.Text)
    thumbnail = db.Column(db.String(255))
    demo_url = db.Column(db.String(255))
    repo_url = db.Column(db.String(255))
    status = db.Column(db.String(50), default="Completed")
    year = db.Column(db.Integer)
    featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    images = db.relationship(
        "ProjectImage",
        backref="project",
        cascade="all, delete-orphan",
        order_by="ProjectImage.display_order",
    )

    @property
    def technologies_list(self):
        return [t.strip() for t in self.technologies.split(",")] if self.technologies else []

    @property
    def features_list(self):
        return [f.strip() for f in self.features.split("\n") if f.strip()] if self.features else []

    def __repr__(self):
        return f"<Project {self.title}>"


class ProjectImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    caption = db.Column(db.String(255))
    display_order = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<ProjectImage {self.image}>"