from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField
from wtforms.validators import DataRequired

class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    sprint_id = SelectField('Sprint', coerce=int)
    person_id = SelectField('Person', coerce=int)

class SprintForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])

class PersonForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
