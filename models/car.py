from db import db
from datetime import datetime
from .rental import Rental

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

    rental = db.relationship("Rental", uselist=False)
    
    
    """rented = db.mapped_column(db.DateTime, nullable=True, default=None)


    def carRent(self):
        self.rented = datetime.now()
        db.session.commit()
    
    def carReturn(self):
        self.rented = None
        db.session.commit()
 """
    
    def makeRental(self, user):
        rental = Rental(car_id=self.id, user_id=user.id, start_date=datetime.now())
        db.session.add(rental)
        db.session.commit()
    def removeRental(self, user):
        statement = db.select(Rental).where(Rental.car_id == self.id)
        rental = db.session.execute(statement).scalar()
        db.session.delete(rental)
        db.session.commit()

