from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, RadioField, BooleanField, SelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput
from wtforms.validators import Required
from flask import session


class MultiCheckboxField(SelectMultipleField):
	widget = ListWidget(prefix_label=False)
	option_widget = CheckboxInput()

class featureForm(FlaskForm):
    options = MultiCheckboxField('options',validators=[Required()])
    submit = SubmitField('Submit')

class sizeForm(FlaskForm):
    size = SelectField('Size',choices=[('10','Top 10'),('20','Top 20'),('all','All')])

class teamForm(FlaskForm):
    team1 = SelectField('Team 1')
    team2 = SelectField('Team 2')
    submit = SubmitField('GO')
