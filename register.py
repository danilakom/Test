from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField


class RegisterForm(FlaskForm):
    email = EmailField("Email")
    password = PasswordField("Password", validators=[DataRequired()])
    r_password = PasswordField("Repeat password", validators=[DataRequired()])
    surname = StringField("Surname")
    name = StringField("Name")
    age = IntegerField("Age")
    position = StringField("Position")
    speciality = StringField("Speciality")
    address = StringField("Address")
    submit = SubmitField("Submit")