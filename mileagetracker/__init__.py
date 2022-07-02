import os 
from flask import Flask
import re 
from flask_sqlalchemy import SQLAlchemy

if os.path.exists("env.py"):
    import env  

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

pg_user = "postgres"
pg_pwd = "Mrdarcy2012??"
pg_port = "5432"
app.config["SQLALCHEMY_DATABASE_URI"] ="postgresql://{username}:{password}@localhost:{port}/mileagetracker".format(username=pg_user, password=pg_pwd, port=pg_port)



db = SQLAlchemy(app)

from mileagetracker import routes 


