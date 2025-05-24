from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db import db
from my_models import User
import os

profile_bp = Blueprint('profile_bp', __name__)

@profile_bp.route("/profile")
def profile():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("login_bp.login"))
    
    usr_stmt = db.select(User).where(User.id == user_id)
    user = db.session.execute(usr_stmt).scalar()

    image_url = None
    if user and user.rental:
        model = user.rental.car.model.replace(" ", "").lower()
        year = str(user.rental.car.year)
        color = user.rental.car.color.replace(" ", "").lower()

        filename = f"{model}_{year}_{color}.png"
        filepath = os.path.join("static", "images", filename)

        if os.path.exists(filepath):
            image_url = url_for("static", filename=f"images/{filename}")
        else:
            image_url = url_for("static", filename="images/default_car.jpg")

    if user:
        return render_template("profile.html", user=user, image_url=image_url)
    else:
        return render_template("error.html")



@profile_bp.route("/profile", methods=["POST"])
def profile_post():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("login_bp.login"))

    usr_stmt = db.select(User).where(User.id == user_id)
    user = db.session.execute(usr_stmt).scalar()

    if user and user.rental:
        user.rental.car.removeRental(user)

    return redirect(url_for("profile_bp.profile"))

