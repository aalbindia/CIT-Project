from db import db
from datetime import datetime

class Car(db.Model):
    __tablename__ = "cars"

    id = db.mapped_column(db.Integer, primary_key=True)
    model = db.mapped_column(db.String, nullable=False)
    year = db.mapped_column(db.Integer, nullable=False)
    color = db.mapped_column(db.String, nullable=False)
    milage = db.mapped_column(db.Integer, nullable=False)
    rate = db.mapped_column(db.Float, nullable=False)
    brand_id = db.mapped_column(db.Integer, db.ForeignKey("brands.id"))
    brand = db.relationship("Brand", back_populates="cars")
    campus_id = db.mapped_column(db.Integer, db.ForeignKey("campuses.id"))
    campus = db.relationship("Campus", back_populates="cars")
    carType_id = db.mapped_column(db.Integer, db.ForeignKey("cartypes.id"))
    carType = db.relationship("CarType", back_populates="cars")

    
    
    """rented = db.mapped_column(db.DateTime, nullable=True, default=None)


    def carRent(self):
        self.rented = datetime.now()
        db.session.commit()
    
    def carReturn(self):
        self.rented = None
        db.session.commit()
 """


