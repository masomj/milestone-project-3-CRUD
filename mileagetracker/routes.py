from turtle import Vec2D
from flask import render_template, request, redirect, url_for
from mileagetracker import app, db
from mileagetracker.models import Vehicles, Mileage
from datetime import datetime

@app.route("/")
def home():
    vehicles = list(Vehicles.query.order_by(Vehicles.vehicle_reg).all())
    return render_template("select_vehicle.html",vehicles=vehicles)


@app.route("/add_mileage/<int:vehicle_id>", methods=["GET","POST"])
def add_mileage(vehicle_id):
    vehicle=Vehicles.query.get_or_404(vehicle_id)
    if request.method == "POST":
        mileage=Mileage(
            start_time = request.form.get("start_time"),
            start_mileage= request.form.get("start_mileage"),
            start_destination= request.form.get("start_destination"),
            end_destination= request.form.get("end_destination"),
            end_mileage= request.form.get("end_mileage"),
            end_time= request.form.get("end_time"),
            vehicle_id = vehicle_id,
            driver = "mason")
        db.session.add(mileage)
        db.session.commit()
        return redirect(url_for("view_vehicle_details"))
    return render_template("add_mileage.html",vehicle=vehicle)


@app.route("/view_vehicle_details/<int:vehicle_id>")
def view_vehicle_details(vehicle_id):
    selected_vehicle = Vehicles.query.get_or_404(vehicle_id)
    mileage_records = list(Mileage.query.filter_by(vehicle_id = vehicle_id).all())
    return render_template("view_vehicle_details.html", mileage=mileage_records, vehicle=selected_vehicle)
    
    