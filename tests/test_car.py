import random
import pytest

class Brand:
    def __init__(self, name):
        if not isinstance(name, str):
            raise TypeError("Brand name must be a string.")
        self.name = name

class Campus:
    def __init__(self, location):
        if not isinstance(location, str):
            raise TypeError("Campus location must be a string.")
        self.location = location

class CarType:
    def __init__(self, type_name):
        self.type_name = type_name

class Car:
    def __init__(self, model, year, color, milage, rate, brand, campus, carType):
        if not isinstance(model, str):
            raise TypeError("Model must be a string.")
        if not isinstance(year, int):
            raise TypeError("Year must be an integer.")
        if not isinstance(color, str):
            raise TypeError("Color must be a string.")
        if not isinstance(milage, int):
            raise TypeError("Milage must be an integer.")
        if not isinstance(rate, (int, float)):
            raise TypeError("Rate must be a number.")
        if not isinstance(brand, Brand):
            raise TypeError("Brand must be a Brand object.")
        if not isinstance(campus, Campus):
            raise TypeError("Campus must be a Campus object.")
        if not isinstance(carType, CarType):
            raise TypeError("CarType must be a CarType object.")
        self.model = model
        self.year = year
        self.color = color
        self.milage = milage
        self.rate = rate
        self.brand = brand
        self.campus = campus
        self.carType = carType

def test_brand():
    brand = Brand(name="Toyota")
    assert brand.name == "Toyota"
    assert isinstance(brand.name, str)

def test_campus():
    campus = Campus(location="Burnaby")
    assert campus.location == "Burnaby"
    assert isinstance(campus.location, str)

def test_car():
    brand = Brand(name="Honda")
    campus = Campus(location="Downtown")
    carType = CarType(type_name="Sedan")
    car = Car(
        model="Civic",
        year=2020,
        color="Blue",
        milage=30000,
        rate=45.5,
        brand=brand,
        campus=campus,
        carType=carType
    )
    assert car.model == "Civic"
    assert isinstance(car.color, str)
    assert isinstance(car.year, int)
    assert isinstance(car.milage, int)
    assert isinstance(car.rate, float)
    assert isinstance(car.brand, Brand)
    assert isinstance(car.campus, Campus)
    assert isinstance(car.carType, CarType)

def test_invalid_brand():
    with pytest.raises(TypeError):
        Brand(name=123)

def test_invalid_campus():
    with pytest.raises(TypeError):
        Campus(location=456)

def test_invalid_car():
    brand = Brand(name="Ford")
    campus = Campus(location="Uptown")
    carType = CarType(type_name="SUV")
    with pytest.raises(TypeError):
        Car(
            model="Explorer",
            year="2021",
            color="Red",
            milage=25000,
            rate=55.0,
            brand=brand,
            campus=campus,
            carType=carType
        )