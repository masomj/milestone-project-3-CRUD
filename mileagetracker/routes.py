from flask import render_template, request, redirect, url_for,flash
from functools import wraps
from mileagetracker import app, db
from mileagetracker.models import Vehicles, Mileage, User
from mileagetracker.forms import LoginForm, RegisterForm
from datetime import date
from flask import Flask
from flask import Flask
from werkzeug.security import generate_password_hash, check_password_hash
import email_validator
from flask_login import login_user,login_required,logout_user,current_user
from flask_login import LoginManager

login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.role != "admin":
            flash("You do not have access to this page. Please contact your Manager for any queries.","Warning")
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    return decorated_view
            

@app.route("/")
def index():
    return redirect(url_for('login'))

@app.route("/login", methods=["GET","POST"])
def login():    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()        
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('home'))
        else:
            flash("Incorrect Username or Password","error")
    return render_template("login.html", form=form)


@app.route("/home")
@login_required
def home():
    vehicles = list(Vehicles.query.order_by(Vehicles.vehicle_reg).all())
    return render_template("select_vehicle.html",vehicles=vehicles)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
    
    
@app.route("/signup", methods=["GET","POST"])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data == form.validatepassword.data:
            hashed_pw = generate_password_hash(form.password.data, method='sha256')
            if current_user.role =='admin':
               new_user= User(
                    username=form.username.data,
                    email=form.email.data,
                    password=hashed_pw,
                    role="User",
                    )                
            else:
                new_user= User(
                    username=form.username.data,
                    email=form.email.data,
                    password=hashed_pw,
                    role=form.role.data,
                    )
                db.session.add(new_user)
                db.session.commit()
                flash("New user added!")
        elif form.password.data != form.validatepassword.data:
            flash("Passwords do not match!","Error")
    return render_template("signup.html", form=form)


@app.route("/add_mileage/<int:vehicle_id>", methods=["GET","POST"])
@login_required
def add_mileage(vehicle_id):
    today=date.today()
    vehicle=Vehicles.query.get_or_404(vehicle_id)
    if Mileage.query.filter_by(vehicle_id=vehicle_id).count() > 0 :
        mileages=list(Mileage.query.filter_by(vehicle_id=vehicle_id).all())
        mileage=mileages[-1]
        if request.method == "POST":
            mileage=Mileage(
                start_time = request.form.get("start_time"),
                start_mileage= request.form.get("start_mileage"),
                start_destination= request.form.get("start_destination"),
                end_destination= request.form.get("end_destination"),
                end_mileage= request.form.get("end_mileage"),
                end_time= request.form.get("end_time"),
                vehicle_id = vehicle_id,
                driver = current_user.username,
                date= today)
            db.session.add(mileage)
            db.session.commit()
            return redirect(url_for("view_vehicle_details",vehicle_id = mileage.vehicle_id))  
        return render_template("add_mileage.html",vehicle=vehicle, mileage=mileage)
    else:    
        if request.method == "POST":
            mileage=Mileage(
                start_time = request.form.get("start_time"),
                start_mileage= request.form.get("start_mileage"),
                start_destination= request.form.get("start_destination"),
                end_destination= request.form.get("end_destination"),
                end_mileage= request.form.get("end_mileage"),
                end_time= request.form.get("end_time"),
                vehicle_id = vehicle_id,
                driver = current_user.username,
                date=today)
            db.session.add(mileage)
            db.session.commit()
            return redirect(url_for("view_vehicle_details",vehicle_id = mileage.vehicle_id))  
    return render_template("add_mileage.html",vehicle=vehicle)


@app.route("/delete_mileage_record/<int:mileage_id>")
@login_required
def delete_mileage_record(mileage_id):
    record=Mileage.query.get_or_404(mileage_id)
    related_vehicle=record.vehicle_id
    db.session.delete(record)
    db.session.commit()
    return redirect(url_for("view_vehicle_details",vehicle_id=related_vehicle))


@app.route("/edit_mileage_record/<int:mileage_id>", methods=["POST","GET"])
@login_required
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
@login_required
def view_vehicle_details(vehicle_id):
    selected_vehicle = Vehicles.query.get_or_404(vehicle_id)
    mileage_records = list(Mileage.query.filter_by(vehicle_id = vehicle_id).all())
    return render_template("view_vehicle_details.html", mileage=mileage_records, vehicle=selected_vehicle)


@app.route("/admin_console")   
@login_required
@admin_required
def admin_console():
    return render_template("admin_console.html")


@app.route("/add_vehicle", methods=["POST","GET"])
@login_required
@admin_required
def add_vehicle():
    if request.method=="POST":
        new_vehicle=Vehicles(vehicle_reg=request.form.get("vehicle_reg"))
        db.session.add(new_vehicle)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add_vehicle.html")


@app.route("/view_vehicle_details_admin")
@login_required
@admin_required
def view_vehicle_details_admin():
    vehicles = list(Vehicles.query.order_by(Vehicles.vehicle_reg).all())
    return render_template("view_vehicle_details_admin.html",vehicles=vehicles)


@app.route("/edit_vehicle/<int:vehicle_id>", methods=["POST","GET"])
@login_required
@admin_required
def edit_vehicle(vehicle_id):
    vehicle = Vehicles.query.get_or_404(vehicle_id)
    if request.method=="POST":
        vehicle.vehicle_reg = request.form.get("vehicle_reg")
        db.session.commit()
        return redirect(url_for('view_vehicle_details_admin'))
    return render_template("edit_vehicle.html",vehicle=vehicle)


@app.route("/delete_vehicle/<int:vehicle_id>")
@login_required
def delete_vehicle(vehicle_id):
    vehicle = Vehicles.query.get_or_404(vehicle_id)
    db.session.delete(vehicle)
    db.session.commit()
    return redirect(url_for('admin_console'))
    


    
    
    