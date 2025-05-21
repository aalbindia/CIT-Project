from flask import Flask, render_template, url_for, redirect, flash, session, request
from pathlib import Path
from db import db
from my_models import Car, Rental, Campus, CarType, User
from auth_decorator import login_required
from dotenv import load_dotenv

from authlib.integrations.flask_client import OAuth
import os
from datetime import timedelta
import random

load_dotenv()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.secret_key = os.getenv("APP_SECRET_KEY")
    if config_name == 'testing':
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        app.config["TESTING"] = True
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.instance_path = Path(".").resolve()

    db.init_app(app)


    return app

app = create_app()

oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'email profile'},
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration'
)

github = oauth.register(
    name='github',
    client_id=os.getenv("GITHUB_CLIENT_ID"),
    client_secret=os.getenv("GITHUB_CLIENT_SECRET"),
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/cars")
def cars():
    sort = request.args.get("sort", "name")
    order = request.args.get("order", "asc")

    statement_car = db.select(Car)


    if sort == "rate": 
        statement_car = statement_car.order_by(Car.rate.desc() if order == "desc" else Car.rate.asc())
    elif sort == "type": 
        statement_car = statement_car.join(Car.carType).order_by(CarType.name.desc() if order == "desc" else CarType.name.asc())
    elif sort == "location": 
        statement_car = statement_car.join(Car.campus).order_by(
        Campus.name.desc() if order == "desc" else Campus.name.asc()
    )




    results = db.session.execute(statement_car)

    return render_template("cars.html", my_list= [prod for prod in results.scalars()], sort_by=sort, order=order)

@app.route("/cars/<int:id>")
def car_details(id):
    statement_car = db.select(Car).where(Car.id == id)
    result = db.session.execute(statement_car).scalar()
    if not result:
        return render_template("error.html", message="order not found"), 404
    
    filename = f"{result.model}_{result.year}_{result.color}.png".replace(" ", "").lower()
    filepath = os.path.join("static", "images", filename)

    
    image_url = f"/static/images/{filename}" if os.path.exists(filepath) else "/static/images/default_car.jpg"


    return render_template("car_details.html", element = result, image_url=image_url)

@app.route("/cars/<int:id>/complete", methods=["POST"])
def rent_car(id):
    statement_car = db.select(Car).where(Car.id == id)
    result = db.session.execute(statement_car).scalar()
    if not result:
        return render_template("error.html", message="order not found"), 404
    
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("login"))
    
    usr_stmt = db.select(User).where(User.id == user_id)
    user = db.session.execute(usr_stmt).scalar()


    if user:
        active_rental_stmt = db.select(Rental).where(Rental.user_id == user.id, Rental.return_date == None)
        active_rental = db.session.execute(active_rental_stmt).scalar()
        if active_rental:
            flash("You already have an active rental. Return it before renting another car.")
            return render_template("car_details.html", element=result)
        result.makeRental(user)
        return render_template("car_details.html", element = result)
    else:
        return render_template("error.html")

 
   
     

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")

    statement_login = db.select(User).where(User.email == email)
    result = db.session.execute(statement_login).scalar()

    if result:
   
        if result.password == password:
            session["user_id"] = result.id
            return redirect(url_for("profile"))
    
    flash('Please check your login details and try again.', "danger")
    return redirect(url_for('login'))
        

@app.route("/google-login")
def google_login():
    redirect_uri = url_for("google_authorize", _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route("/google-authorize")
def google_authorize():
    token = google.authorize_access_token()
    resp = google.get("userinfo")
    user_info = resp.json()
    email = user_info["email"]

    statement = db.select(User).where(User.email == email)
    user = db.session.execute(statement).scalar()

    if not user:
        chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        random_string = ''.join(random.choices(chars, k=10))
        name = user_info["name"]
        user = User(email=email, password=random_string, username=name)
        db.session.add(user)
        db.session.commit()

    session["user_id"] = user.id
    session.permanent = True
    return redirect(url_for("profile"))



@app.route("/github-login")
def github_login():
    redirect_uri = url_for("github_authorize", _external=True)
    return github.authorize_redirect(redirect_uri)

@app.route("/github-authorize")
def github_authorize():
    token = github.authorize_access_token()
    resp = github.get("user")  
    user_info = resp.json()

    email = user_info.get("email")
    if not email:
        email_resp = github.get("user/emails")
        emails = email_resp.json()
        primary_emails = [e for e in emails if e.get("primary") and e.get("verified")]
        if primary_emails:
            email = primary_emails[0].get("email")

    name = user_info.get("name") or user_info.get("login")

    statement = db.select(User).where(User.email == email)
    user = db.session.execute(statement).scalar()
    if not user:
        chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        random_string = ''.join(random.choices(chars, k=10))

        user = User(email=email, name=name, password=random_string)
        db.session.add(user)
        db.session.commit()

    session["user_id"] = user.id
    session.permanent = True
    return redirect(url_for("profile"))


@app.route("/signup")
def signup():


    return render_template("signup.html")


@app.route("/signup", methods=["POST"])
def signup_post():
    email = request.form.get("email")
    password = request.form.get("password")
    name = request.form.get("name")

    statement_login = db.select(User).where(User.email == email)
    result = db.session.execute(statement_login).scalar()

    if not result:
        
        newuser = User(username=name, email=email, password=password)
        db.session.add(newuser)
        db.session.commit()

        session["user_id"] = newuser.id
        session.permanent = True

        return redirect(url_for("profile"))
    flash('A user with that email already exists.')
    return redirect(url_for('signup'))


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("login"))



@app.route("/profile")
def profile():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("login"))
    
    usr_stmt = db.select(User).where(User.id == user_id)
    user = db.session.execute(usr_stmt).scalar()
    if user:
        return render_template("profile.html", user=user)
    else:
        return render_template("error.html")


@app.route("/profile",  methods=["POST"])
def profile_post():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("login"))
    
    usr_stmt = db.select(User).where(User.id == user_id)
    user = db.session.execute(usr_stmt).scalar()
    if user:
        user.rental.car.removeRental(user)
        return render_template("profile.html", user=user)
    else:
        return render_template("error.html")




if __name__ == "__main__":
    app.run(debug=True, port=8888)