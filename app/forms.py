from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, Form, validators, SelectField
from wtforms.validators import InputRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[InputRequired()])
    lastname = StringField('Last Name', validators=[InputRequired()])
    age = IntegerField('Age', validators=[InputRequired()])
    gender = SelectField('Gender', choices=[('Female', 'Male', 'Other')])
    bio = StringField('Biography',validators.Length(max= 240))