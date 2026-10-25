from flask import Blueprint, render_template, request, jsonify
from app.forms import ContactForm
from app.extensions import db
from app.models import ContactMessage

contact_bp = Blueprint("contact", __name__)


@contact_bp.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        if form.honeypot.data:
            return jsonify({"success": True})

        new_message = ContactMessage(
            name=form.name.data,
            email=form.email.data,
            subject=form.subject.data,
            message=form.message.data,
        )
        db.session.add(new_message)
        db.session.commit()

        return jsonify({"success": True})

    if request.method == "POST":
        return jsonify({"success": False, "errors": form.errors}), 400

    return render_template("contact.html", form=form)