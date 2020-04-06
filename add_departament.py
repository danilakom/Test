from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField, IntegerField, StringField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class Add_Departament(FlaskForm):
    title = StringField("Название", validators=[DataRequired()])
    chief = IntegerField("id главного", validators=[DataRequired()])
    members = StringField("Члены")
    email = EmailField("Email")
    submit = SubmitField("Подтвердить")
