import os 
from flask import Flask
import re 
from flask_sqlalchemy import SQLAlchemy



if os.path.exists("env.py"):
    import env  

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
print(os.environ.get("DATABASE_URL"))

db = SQLAlchemy(app)



from mileagetracker import routes 


