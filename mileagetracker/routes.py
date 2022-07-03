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
    mileage=list(Mileage.query.filter_by(vehicle_id=vehicle_id).first())
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
        return redirect(url_for("home"))
    return render_template("add_mileage.html",vehicle=vehicle)


@app.route("/delete_mileage_record/<int:mileage_id>")
def delete_mileage_record(mileage_id):
    record=Mileage.query.get_or_404(mileage_id)
    related_vehicle=record.vehicle_id
    db.session.delete(record)
    db.session.commit()
    return redirect(url_for("view_vehicle_details",vehicle_id=related_vehicle))


@app.route("/edit_mileage_record/<int:mileage_id>", methods=["POST","GET"])
def edit_mileage_record(mileage_id):
    mileage= Mileage.query.get_or_404(mileage_id)
    vehicle= Vehicles.query.get_or_404(mileage.vehicle_id)
    if request.method == "POST":
            mileage.start_time = request.form.get("start_time")
            mileage.start_mileage= request.form.get("start_mileage")
            mileage.start_destination= request.form.get("start_destination")
            mileage.end_destination= request.form.get("end_destination")
            mileage.end_mileage= request.form.get("end_mileage")
            mileage.end_time= request.form.get("end_time")
            db.session.commit()
            return redirect(url_for("view_vehicle_details",vehicle_id = mileage.vehicle_id))
    return render_template("edit_mileage_record.html",mileage = mileage,vehicle=vehicle)

    
@app.route("/view_vehicle_details/<int:vehicle_id>")
def view_vehicle_details(vehicle_id):
    selected_vehicle = Vehicles.query.get_or_404(vehicle_id)
    mileage_records = list(Mileage.query.filter_by(vehicle_id = vehicle_id).all())
    return render_template("view_vehicle_details.html", mileage=mileage_records, vehicle=selected_vehicle)


@app.route("/admin_console")   
def admin_console():
    return render_template("admin_console.html")


@app.route("/add_vehicle", methods=["POST","GET"])
def add_vehicle():
    if request.method=="POST":
        new_vehicle=Vehicles(vehicle_reg=request.form.get("vehicle_reg"))
        db.session.add(new_vehicle)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("edit_vehicle.html")


@app.route("/view_vehicle_details_admin")
def view_vehicle_details_admin():
    vehicles = list(Vehicles.query.order_by(Vehicles.vehicle_reg).all())
    return render_template("view_vehicle_details_admin.html",vehicles=vehicles)


@app.route("/edit_vehicle/<int:vehicle_id>", methods=["POST","GET"])
def edit_vehicle(vehicle_id):
    vehicle = Vehicles.query.get_or_404(vehicle_id)
    if request.method=="POST":
        selected_vehicle.vehicle_reg = request.form.get("vehicle_reg")
    return render_template("edit_vehicle.html",vehicle=vehicle)


@app.route("/delete_vehicle/<int:vehicle_id>")
def delete_vehicle(vehicle_id):
    vehicle = Vehicles.query.get_or_404(vehicle_id)
    db.session.delete(vehicle)
    db.session.commit()
    return redirect(url_for('admin_console'))
    
    

    
    
    