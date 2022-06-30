from flask import render_template, request, redirect, url_for
from mileagetracker import app, db
from mileagetracker.models import Vehicles, Mileage


@app.route("/")
def home():
    return render_template("base.html")
    