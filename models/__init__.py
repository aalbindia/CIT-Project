from db import db

__all__ = ["Car", "Brand", "Campus", "CarType", "User", "Rental"]

from .user import User
from .brand import Brand
from .campus import Campus
from .carType import CarType
from .car import Car
from .rental import Rental