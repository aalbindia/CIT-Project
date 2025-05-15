from db import db

class Campus(db.Model):
    __tablename__ = "campuses"

    id = db.mapped_column(db.Integer, primary_key=True)
    name = db.mapped_column(db.String)
    cars = db.relationship("Car", back_populates="campus")
