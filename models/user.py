from db import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"

    id = db.mapped_column(db.Integer, primary_key=True)
    username = db.mapped_column(db.String, nullable=False, unique=True)
    email = db.mapped_column(db.String, nullable=False, unique=True)
    password = db.mapped_column(db.String, nullable=False)