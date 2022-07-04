from xmlrpc.client import Boolean
from flask_wtf import FlaskForm
from flask import Flask
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email,Length

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(),Length(min=4,max=15)])
    password = PasswordField('password', validators=[InputRequired(),Length(min=4,max=80)])
    remember = BooleanField('remember me')