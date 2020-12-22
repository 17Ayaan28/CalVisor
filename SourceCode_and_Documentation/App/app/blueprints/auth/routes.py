from app import db
from . import auth
from app.Classes.Models import User
from .forms import LoginForm, RegistrationForm, ChangePasswordForm
from flask import render_template, session, redirect, url_for, current_app
from flask_login import current_user, login_user, login_required, logout_user

@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user_email = login_form.email.data
        user = User.query.filter_by(email=user_email).first()
        if user is not None and user.password == login_form.password.data:
            login_user(user, login_form.remember_me.data)
            return redirect(url_for('main.dashboard'))
    return render_template('auth/login.html', form=login_form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegistrationForm()
    if register_form.validate_on_submit():
        new_user = User(email=register_form.email.data,
                        username = register_form.username.data,
                        password = register_form.password.data,
                        profile_settings = register_form.profile_settings.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('main.home_page'))
    return render_template('auth/register.html',form=register_form)

@auth.route('/change-password', methods=['GET', 'POST'])
def change_password():
    change_password_form = ChangePasswordForm()
    if change_password_form.validate_on_submit():
        user_email = change_password_form.email.data
        user = User.query.filter_by(email=user_email).first()
        if user is not None:
            user.password = change_password_form.new_password.data
            db.session.commit()
        return redirect(url_for('main.home_page'))
    return render_template('auth/change-password.html', form=change_password_form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home_page'))
