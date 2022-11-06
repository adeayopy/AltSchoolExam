from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskexam.models import User
# from flaskclass.users.routes import users

class RegisterationForm(FlaskForm):
    username=StringField('Username', 
    validators=[DataRequired(),Length(min=2, max=30) ])
    firstname=StringField('Firstname', 
    validators=[DataRequired(),Length(min=2, max=30) ])
    lastname=StringField('Lastname', 
    validators=[DataRequired(),Length(min=2, max=30) ])
    email=StringField('Email',
    validators=[DataRequired(), Email() ])
    password=PasswordField('Password',
    validators=[DataRequired()])
    confirm_password=PasswordField('Confirm password', 
    validators=[DataRequired(), EqualTo('password')])
    submit=SubmitField('Sign up')

    def validate_username(self,username):
        # app_context():
        user=User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken, please choose a different one')

    def validate_email(self,email):
        # with users.app_context():
        user=User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken, please use a different one')

class LoginForm(FlaskForm):
    email=StringField('Email',
    validators=[DataRequired(), Email() ])
    password=PasswordField('Password',
    validators=[DataRequired()])
    remember=BooleanField('Remember me')
    submit=SubmitField('Login')

class UpdateForm(FlaskForm):
    username=StringField('Username', 
    validators=[DataRequired(),Length(min=2, max=30) ])
    email=StringField('Email',
    validators=[DataRequired(), Email() ])
    firstname=StringField('Firstname', 
    validators=[DataRequired(),Length(min=2, max=30) ])
    lastname=StringField('Lastname', 
    validators=[DataRequired(),Length(min=2, max=30) ])
    picture=FileField('Update profile picture', validators=[FileAllowed(['jpg','png'])])
    submit=SubmitField('Update')

    def validate_username(self,username):
        if username.data!=current_user.username:
            # with users.app_context():
            user=User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken, please choose a different one')

    def validate_email(self,email):
        if email.data!=current_user.email:
            # with users.app_context():
            user=User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken, please use a different one')

class RequestResetForm(FlaskForm):
    email=StringField('Email',
    validators=[DataRequired()])
    submit=SubmitField('Request Password Request')
    def validate_email(self,email):
        # with app.app_context():
        user=User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with this email. Register first')

class ResetPasswordForm(FlaskForm):
    password=PasswordField('Password',
    validators=[DataRequired()])
    confirm_password=PasswordField('Confirm password', 
    validators=[DataRequired(), EqualTo('password')])
    submit=SubmitField('Reset Password')
   