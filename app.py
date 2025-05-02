from flask import Flask, render_template, url_for, redirect
from pathlib import Path
#import datetime 
from db import db
from models import *

from flask import request

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

    statement_car = db.select(Car)

    results = db.session.execute(statement_car)

    return render_template("cars.html", my_list= [prod for prod in results.scalars()])

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
    
    if not result.rented:
        result.carRent()
    else:
        result.carReturn()
   
    return render_template("car_details.html", element = result)


if __name__ == "__main__":
    app.run(debug=True, port=8888)