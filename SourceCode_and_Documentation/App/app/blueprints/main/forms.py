from flask_wtf import FlaskForm
from app.Classes.Models import User
from flask_login import current_user
from wtforms.widgets import PasswordInput
from wtforms import BooleanField, SubmitField, StringField, SelectField, PasswordField, IntegerField
from wtforms.fields.html5 import DateField, TimeField
from wtforms.validators import DataRequired, Length, Email, ValidationError, NumberRange, InputRequired, EqualTo
import re
import datetime

class ChangePrivacyForm (FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Password', validators=[DataRequired()])
    profile_settings =BooleanField('New Profile Settings')
    submit = SubmitField('Update Privacy',
            render_kw={'style':'background:linear-gradient(to bottom right, #344CD1, #B3BEFF);color:white; border-radius:25px;width:100%;font-weight:bold;'}
    )

class ChangeUsernameForm (FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Password', validators=[DataRequired()])
    new_username = StringField('New Username ', validators=[DataRequired(), Length(1, 64)])
    submit = SubmitField('Update Username',
            render_kw={'style':'background:linear-gradient(to bottom right, #344CD1, #B3BEFF);color:white; border-radius:25px;width:100%;font-weight:bold;'}
    )

class ChangeEmailForm (FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Password', validators=[DataRequired()])
    new_email = StringField('New Email', validators=[DataRequired(), Length(1, 64), Email()])
    submit = SubmitField('Update Email',
            render_kw={'style':'background:linear-gradient(to bottom right, #344CD1, #B3BEFF);color:white; border-radius:25px;width:100%;font-weight:bold;'}
    )

class ChangeKnownPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    new_password_confirm = PasswordField('Confirm New Password', validators=[DataRequired()])
    submit = SubmitField('Update Password',
            render_kw={'style':'background:linear-gradient(to bottom right, #344CD1, #B3BEFF);color:white; border-radius:25px;width:100%;font-weight:bold;'}
    )


class NewEventForm(FlaskForm):

    name = StringField('Name', validators=[DataRequired(), Length(1, 64)])
    addr = StringField('Address', validators=[DataRequired(), Length(1, 128)])
    date = DateField("Date ", format='%Y-%m-%d', validators=[DataRequired()])
    start_time = TimeField("Start Time", format='%H:%M', validators=[InputRequired()])
    end_time = TimeField("End Time", format='%H:%M', validators=[InputRequired()])
    repeating_event = BooleanField('Repeating Event')
    submit = SubmitField("Add Event",
            render_kw={'style':'background:linear-gradient(to bottom right, #344CD1, #B3BEFF);color:white; border-radius:25px;width:100%;font-weight:bold;'}
    )

    def validate_date(self, field):
        if(field.data < datetime.datetime.now().date()):
            raise ValidationError("Date has passed")

    def validate_start_time(self, field):
        if(self.end_time.data <= field.data):
            raise ValidationError("Start Time must be before End Time")

class InviteForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Length(1,64), Email()])
    submit = SubmitField("Invite",
            render_kw={'style':'background:linear-gradient(to bottom right, #344CD1, #B3BEFF);color:white; border-radius:25px;width:100%;font-weight:bold;'}
    )

    def validate_email(self, field):
        if not User.query.filter_by(email=field.data).first():
            raise ValidationError('Email does not exist')

class RecommendationForm(FlaskForm):

    place_type = SelectField("I want to", choices =[('food', 'Eat')])
    day = SelectField('On', choices=[('0', 'MON'),
                                     ('1', 'TUE'),
                                     ('2', 'WED'),
                                     ('3', 'THU'),
                                     ('4', 'FRI'),
                                     ('5', 'SAT'),
                                     ('6', 'SUN')])
    radius = IntegerField('Radius (metres)', validators=[DataRequired(), NumberRange(min=1, max=40000, message='Must be between 1 & 40km')])
    submit = SubmitField("Get Recommendations",
            render_kw={'style':'background:linear-gradient(to bottom right, #344CD1, #B3BEFF);color:white; border-radius:25px;width:100%;font-weight:bold;'}
    )

    def validate_email(self, field):
        if not User.query.filter_by(email=field.data).first():
            raise ValidationError('Email does not exist')

class EditEventForm(FlaskForm):

    name = StringField('Name', validators=[DataRequired(), Length(1, 64)])
    addr = StringField('Address', validators=[DataRequired(), Length(1, 128)])
    date = DateField("Date ", format='%Y-%m-%d', validators=[DataRequired()])
    start_time = TimeField("Star Time", format='%H:%M', validators=[InputRequired()])
    end_time = TimeField("End Time", format='%H:%M', validators=[InputRequired()])
    repeating_event = BooleanField('Repeating Event')
    submit = SubmitField("Update",
            render_kw={'style':'background:linear-gradient(to bottom right, #344CD1, #B3BEFF);color:white; border-radius:25px;width:100%;font-weight:bold;'}
    )

class ChangeDetailsForm(FlaskForm):
    email = StringField('New Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('New Username ', validators=[DataRequired(), Length(1, 64)])
    password1 = PasswordField('New Password', widget=PasswordInput(hide_value=False), validators=[DataRequired(), EqualTo('password2', message='Password Must Match')])
    password2 = PasswordField('Confirm New Password', widget=PasswordInput(hide_value=False), validators=[DataRequired()])
    privacy =BooleanField('Private Account')
    submit = SubmitField('Update Details',
            render_kw={'style':'background:linear-gradient(to bottom right, #344CD1, #B3BEFF);color:white; border-radius:25px;width:100%;font-weight:bold;'}
    )

    def validate_email(self, field):
        if field.data != current_user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError("Email Already Exists")
    def validate_username(self, field):
        if field.data != current_user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError("Username Already Exists")

class FormDefaults:
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', None)
        self.addr = kwargs.get('addr', None)
        self.date = kwargs.get('date', None)
        self.start_time = kwargs.get('start_time', None)
        self.end_time = kwargs.get('end_time', None)
        self.repeating_event = kwargs.get('repeating_event', None)
        self.submit = kwargs.get('submit', None)

class DefaultDetails:
    def __init__(self, **kwargs):
        self.email = kwargs.get('email', None)
        self.username = kwargs.get('username', None)
        self.password1 = kwargs.get('password1', None)
        self.password2 = kwargs.get('password2', None)
        self.privacy = kwargs.get('privacy', False)
