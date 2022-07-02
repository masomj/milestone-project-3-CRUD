from turtle import Vec2D
from flask import render_template, request, redirect, url_for
from mileagetracker import app, db
from mileagetracker.models import Vehicles, Mileage
from datetime import datetime


@app.route("/")
def home():
    vehicles = list(Vehicles.query.order_by(Vehicles.vehicle_reg).all())
    return render_template("select_vehicle.html",vehicles=vehicles)

@app.route("/add_mileage", methods=["GET","POST"])
def add_mileage():
    
    if request.method == "POST":
        return render_template("add_mileage.html", datetime=str(datetime.now()))