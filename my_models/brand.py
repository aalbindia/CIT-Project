from db import db

class Brand(db.Model):
    __tablename__ = "brands"

    id = db.mapped_column(db.Integer, primary_key=True)
    name = db.mapped_column(db.String)
    cars = db.relationship("Car", back_populates="brand")

