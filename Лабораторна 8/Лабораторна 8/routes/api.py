from flask import Blueprint, render_template, redirect, url_for, request
from models import db, Order, Feedback
api_bp = Blueprint("api", __name__, url_prefix="/api")
admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/")
def admin_panel():
    orders = Order.query.all()
    feedback = Feedback.query.all()
    return render_template("admin.html", orders=orders, feedback=feedback)
@admin_bp.route("/delete_feedback/<int:id>", methods=["POST"])
def delete_feedback(id):
    fb = Feedback.query.get_or_404(id)
    db.session.delete(fb)
    db.session.commit()
    return redirect(url_for("admin.admin_panel"))   

@api_bp.route("/products")
def get_products():
    return {"products": ["Apple", "Banana", "Orange"]}

@api_bp.route("/feedback")
def get_feedback():
    return {"feedback": ["Добре", "Погано"]}