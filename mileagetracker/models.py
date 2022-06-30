from enum import unique
from lib2to3.pgen2 import driver
from mileagetracker import db



class Vehicles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_reg = db.Column(db.String(7), unique=True, nullable=False)
    mileage_records = db.relationship("mileage", backref="vehicle", cascade="all, delete", lazy=True)


class Mileage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.Time, nullable=False)
    start_mileage= db.Column(db.Integer, nullable=False)
    start_destination= db.Column(db.String, nullable=False)
    end_destination= db.Column(db.String, nullable=False)
    end_mileage= db.Column(db.Integer, nullable=False)
    end_time= db.Column(db.Time, nullable=False)
    driver= db.Column(db.String, nullable=False)
    vehicle_id= db.Column(db.String, db.ForeignKey("vehicle.id", ondelete="CASCADE"), nullable=False)

