from . import auth
from .forms import loginForm, registerForm
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required
from ..models import User
from .. import db



@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = loginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = registerForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            if form.password.data == form.password2.data:
                user = User(username=form.username.data, password=form.password.data)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('auth.login'))
            else:
                flash('Passwords do not match')
        else:
            flash('Username Already Taken')
    return render_template('auth/register.html', form=form)
