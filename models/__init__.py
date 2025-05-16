from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

__all__ = ["Car", "Brand", "Campus", "CarType", "User", "Rental"]

# Import models after db is defined to avoid circular imports
from .user import User
from .brand import Brand
from .campus import Campus
from .carType import CarType
from .car import Car
from .rental import Rental