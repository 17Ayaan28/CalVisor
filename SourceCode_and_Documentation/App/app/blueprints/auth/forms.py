from flask_wtf import FlaskForm
from app.Classes.Models import User
from flask_login import current_user
from wtforms.validators import DataRequired, Length, Email, EqualTo, InputRequired
from wtforms import StringField, BooleanField, PasswordField, SubmitField, ValidationError

class LoginForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField("Keep me logged in")

    submit = SubmitField(
            'Log in',
            render_kw={'style':'background:linear-gradient(to bottom right, #344CD1, #B3BEFF);color:white; border-radius:25px;width:100%;font-weight:bold;'}
    )

class RegistrationForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Password', validators=[InputRequired(), EqualTo('password2', message='passwords must match')])
    password2 = PasswordField('Confirm Password')
    profile_settings =BooleanField('Make my account private')
    submit = SubmitField(
            'Register',
            render_kw={'style':'background:linear-gradient(to bottom right, #344CD1, #B3BEFF);color:white; border-radius:25px;width:100%;font-weight:bold;'}
    )

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already Exists')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already Exists')

class ChangePasswordForm (FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(1, 64)])
    new_password = PasswordField('New Password',
                             validators=[InputRequired(), EqualTo('new_password2', message='passwords must match')])
    new_password2 = PasswordField('Confirm New Password')
    submit = SubmitField(
            'Change Password',
            render_kw={'style':'background:linear-gradient(to bottom right, #344CD1, #B3BEFF);color:white; border-radius:25px;width:100%;font-weight:bold;'}
    )
