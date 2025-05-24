from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db import db
from my_models import User

signup_bp = Blueprint('signup_bp', __name__)

@signup_bp.route("/signup")
def signup():


    return render_template("signup.html")


@signup_bp.route("/signup", methods=["POST"])
def signup_post():
    email = request.form.get("email")
    password = request.form.get("password")
    name = request.form.get("name")

    statement_login = db.select(User).where(User.email == email)
    result = db.session.execute(statement_login).scalar()
    if "@" not in email:
        flash('Email is not valid.', 'danger')
        return render_template('signup.html')
    
    has_letter = any(c.isalpha() for c in password)
    has_digit = any(c.isdigit() for c in password)
    if len(password) < 8 or not has_letter or not has_digit:
        flash('Password must be at least 8 characters and include both letters and numbers.', 'danger')
        return render_template('signup.html')
    if not result:
        
        newuser = User(username=name, email=email, password=password)
        db.session.add(newuser)
        db.session.commit()

        session["user_id"] = newuser.id
        session.permanent = True

        return redirect(url_for("profile_bp.profile"))
    flash('A user with that email already exists.', 'danger')
    return render_template('signup.html')