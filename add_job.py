from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField, IntegerField, StringField
from wtforms.validators import DataRequired


class Add_Job(FlaskForm):
    team_leader = IntegerField('id лидера', validators=[DataRequired()])
    job = StringField('Работа', validators=[DataRequired()])
    work_size = IntegerField('Длительность')
    collaborators = StringField('Напарники')
    start_date = StringField('Дата начала(день.месяц.год часы:минуты:секунды)')
    end_date = StringField('Дата окончания(день.месяц.год часы:минуты:секунды)')
    is_finished = BooleanField('Закончена?')
    submit = SubmitField('Добавить')