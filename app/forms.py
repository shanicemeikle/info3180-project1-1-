from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, Form, validators, SelectField
from wtforms.validators import InputRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[InputRequired()])
    lastname = StringField('Last Name', validators=[InputRequired()])
    age = IntegerField('Age', validators=[InputRequired()])
    gender = SelectField('Gender', choices=[('Female', 'Male', 'Other')])
    bio = StringField('Biography',validators.Length(max= 240))
    profile_form = FileField("Image", validators = [FileRequired(), FileAllowed(['jpeg','jpg','png'])])