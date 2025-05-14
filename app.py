from flask import Flask, render_template, url_for, redirect, flash, session
from pathlib import Path
#import datetime 
from db import db
from models import *


from auth_decorator import login_required

from flask import request

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# This will make Flask use a 'sqlite' database with the filename provided
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"


# This will make Flask store the database file in the path provided
app.instance_path = Path(".").resolve()

db.init_app(app)

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
    return render_template("car_details.html", element = result)

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
    flash('Please check your login details and try again.')
    return redirect(url_for('login'))
        

@app.route("/signup")
def signup():


    return render_template("signup.html")


@app.route("/signup", methods=["POST"])
def signup_post():


    return "pee"

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