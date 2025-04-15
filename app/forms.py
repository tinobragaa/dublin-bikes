from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, EqualTo, ValidationError


class SignupForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm = PasswordField('Confirm Password', validators=[
        InputRequired(), EqualTo('password', message='Passwords must match.')
    ])
    submit = SubmitField('Sign Up')
    def validate_email(self, field):
        if not field.data.endswith('@gmail.com'):
            raise ValidationError('Please enter a valid Gmail address (must end with @gmail.com).')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Log in')
