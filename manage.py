from db import db
from models import Car, Campus, Brand, CarType
import sys
from app import app
import csv

def createDB():
    db.create_all()

def delDB():
    db.drop_all()

def readData():
    with open("cars.csv", 'r') as file:
        reader = csv.DictReader(file)
        print(reader)
        
        for row in reader:
            tables = {"brand": Brand, "campus": Campus, "CarType": CarType }
            values = {}
            for key, object in tables.items():
                result = db.session.execute(
                    db.select(object).where(object.name == row[key])
                )
                obj = result.scalar()

                if not obj:
                    obj = object(name=row[key])
                    db.session.add(obj)
                
                values[key] = obj

            car = Car(
            model=row["model"],
            year=row["year"],
            color=row["color"],
            milage=row["milage"],
            rate=row["rate"],
            brand=values["brand"],
            campus=values["campus"],
            carType=values["CarType"]
            )
            

            db.session.add(car)

        db.session.commit()

def refresh():
    delDB()
    createDB()
    readData()







if __name__ == "__main__":
    with app.app_context():
        command = sys.argv[1]
        if command == "drop":
            delDB()
        elif command == "create":
            createDB()
        elif command == "read":
            readData()
        elif command == "default":
            refresh()
        else:
            print("Valid arguments are: 'drop', 'create', 'gen <int>', 'default'")
        