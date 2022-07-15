import os 
from flask import Flask
import re 
from flask_sqlalchemy import SQLAlchemy



if os.path.exists("env.py"):
    import env  

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

if os.environ.get("DEVELOPMENT") == "True":

    pg_user = "postgres"
    pg_pwd = "Mrdarcy2012??"
    pg_port = "5432"
    app.config["SQLALCHEMY_DATABASE_URI"] ="postgresql://{username}:{password}@localhost:{port}/mileagetracker".format(username=pg_user, password=pg_pwd, port=pg_port)
else:
    uri = os.environ.get("DATABASE_URL")
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://",1)
    app.config["SQLALCHEMY_DATABASE_URI"] = uri

db = SQLAlchemy(app)



from mileagetracker import routes 


