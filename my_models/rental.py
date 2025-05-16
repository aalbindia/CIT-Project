from db import db
from datetime import datetime

class Rental(db.Model):
    __tablename__ = "rentals"

    id = db.mapped_column(db.Integer, primary_key=True)
    
    car_id = db.mapped_column(db.Integer, db.ForeignKey("cars.id"), nullable=False)
    car = db.relationship("Car", back_populates='rental')
    
    user_id = db.mapped_column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates='rental')

    start_date = db.mapped_column(db.DateTime, nullable=False)
    return_date = db.mapped_column(db.DateTime, nullable=True, default=None)