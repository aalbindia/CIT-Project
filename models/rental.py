from db import db
from datetime import datetime

class Rental(db.Model):
    __tablename__ = "rentals"

    id = db.mapped_column(db.Integer, primary_key=True)
    
    car_id = db.mapped_column(db.Integer, db.ForeignKey("cars.id"))
    car = db.relationship("Car")
    user_id = db.mapped_column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User")

    start_date = db.mapped_column(db.DateTime, nullable=False)
    return_date = db.mapped_column(db.DateTime, nullable=True, default=None)