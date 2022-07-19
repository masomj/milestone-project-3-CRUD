from flask_wtf import FlaskForm
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import InputRequired, Email,Length,EqualTo

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(),Length(min=4,max=15)])
    password = PasswordField('Password', validators=[InputRequired(),Length(min=8,max=256)])
    
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(),Length(min=4,max=15)])
    password = PasswordField('New Password', [InputRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm  = PasswordField('Repeat Password')
    email = StringField('Email', validators=[InputRequired(),Email(message='Invalid'),Length(max=50)])
    role = SelectField('Role', choices = [('admin', 'Admin'),('user', 'Standard User')]) 