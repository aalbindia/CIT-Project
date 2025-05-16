from db import db

class CarType(db.Model):
    __tablename__ = "cartypes"

    id = db.mapped_column(db.Integer, primary_key=True)
    name = db.mapped_column(db.String)
    cars = db.relationship("Car", back_populates="carType")
  

