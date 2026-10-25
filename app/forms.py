from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, SelectField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Email, Length, Optional, URL


class ContactForm(FlaskForm):
    name = StringField("Nama", validators=[DataRequired(message="Nama wajib diisi."), Length(max=100)])
    email = StringField("Email", validators=[DataRequired(message="Email wajib diisi."), Email(message="Format email tidak valid."), Length(max=120)])
    subject = StringField("Subjek", validators=[DataRequired(message="Subjek wajib diisi."), Length(max=150)])
    message = TextAreaField("Pesan", validators=[DataRequired(message="Pesan tidak boleh kosong."), Length(max=2000)])
    honeypot = StringField("Jangan isi kolom ini")
    submit = SubmitField("Kirim Pesan")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(message="Username wajib diisi.")])
    password = PasswordField("Password", validators=[DataRequired(message="Password wajib diisi.")])
    submit = SubmitField("Login")


class ProjectForm(FlaskForm):
    title = StringField("Judul", validators=[DataRequired(message="Judul wajib diisi."), Length(max=150)])
    slug = StringField("Slug (untuk URL)", validators=[DataRequired(message="Slug wajib diisi."), Length(max=150)])
    category = SelectField(
        "Kategori",
        choices=[
            ("Web Development", "Web Development"),
            ("Mobile Development", "Mobile Development"),
            ("Backend", "Backend"),
            ("UI/UX", "UI/UX"),
        ],
        validators=[DataRequired()],
    )
    short_description = TextAreaField("Deskripsi Singkat", validators=[DataRequired(message="Deskripsi singkat wajib diisi."), Length(max=300)])
    role = StringField("Peran", validators=[Optional(), Length(max=150)])
    problem = TextAreaField("Masalah", validators=[Optional()])
    solution = TextAreaField("Solusi", validators=[Optional()])
    challenges = TextAreaField("Tantangan", validators=[Optional()])
    results = TextAreaField("Hasil & Pembelajaran", validators=[Optional()])
    technologies = StringField("Teknologi (pisahkan dengan koma)", validators=[Optional()])
    features = TextAreaField("Fitur Utama (satu per baris)", validators=[Optional()])
    demo_url = StringField("Link Demo", validators=[Optional(), URL(message="URL tidak valid."), Length(max=255)])
    repo_url = StringField("Link Repository", validators=[Optional(), URL(message="URL tidak valid."), Length(max=255)])
    status = SelectField(
        "Status",
        choices=[("Completed", "Completed"), ("In Progress", "In Progress"), ("Archived", "Archived")],
        validators=[DataRequired()],
    )
    year = IntegerField("Tahun", validators=[Optional()])
    featured = BooleanField("Tandai sebagai proyek unggulan")
    thumbnail = FileField(
        "Thumbnail (JPG/PNG/WEBP, maks 5MB)",
        validators=[FileAllowed(["jpg", "jpeg", "png", "webp"], message="Format file harus JPG, PNG, atau WEBP.")],
    )
    submit = SubmitField("Simpan")