from enum import unique
from lib2to3.pgen2 import driver
from mileagetracker import db
from flask_login import UserMixin


class Vehicles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_reg = db.Column(db.String(7), unique=True, nullable=False)
    mileage = db.relationship('Mileage',backref="vehicles", cascade="all, delete", lazy=True)
    
class Mileage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.Time, nullable=False)
    start_mileage= db.Column(db.Integer, nullable=False)
    start_destination= db.Column(db.String, nullable=False)
    end_destination= db.Column(db.String, nullable=False)
    end_mileage= db.Column(db.Integer, nullable=False)
    end_time= db.Column(db.Time, nullable=False)
    driver= db.Column(db.String, nullable=False)
    vehicle_id= db.Column(db.Integer, db.ForeignKey("vehicles.id", ondelete="CASCADE"), nullable=False)
    date=db.Column(db.Date,nullable=False)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(256))
    roles = db.relationship('Role', secondary='user_roles',backref="users")

# Define the Role data-model
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

# Define the UserRoles association table
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))

