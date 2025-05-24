from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db import db
from my_models import User

login_bp = Blueprint('login_bp', __name__)

@login_bp.route("/login")
def login():
    return render_template("login.html")

@login_bp.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")

    statement_login = db.select(User).where(User.email == email)
    result = db.session.execute(statement_login).scalar()

    if result:
   
        if result.password == password:
            session["user_id"] = result.id
            return redirect(url_for("profile_bp.profile"))
    
    flash('Please check your login details and try again.', "danger")
    return redirect(url_for('login_bp.login'))
        