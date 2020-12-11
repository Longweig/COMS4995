from . import web
from freefree.app.libs.email import send_email
from freefree.app.models.base import db
from freefree.app.models.user import User
from flask import render_template, request, redirect, url_for, flash
from freefree.app.forms.auth import RegisterForm, LoginForm, \
    EmailForm, ResetPasswordForm, ChangePasswordForm
from flask_login import login_user, logout_user, login_required, current_user


@web.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        with db.auto_commit():
            user = User()
            user.set_attrs(form.data)
            db.session.add(user)
        return redirect(url_for('web.login'))
    return render_template('auth/register.html', form=form)


@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('web.index')
            return redirect(next_page)
        else:
            flash("Sorry, this does not match our records. \
             Check the spelling and try again.")
    return render_template('auth/login.html', form=form)


@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    form = EmailForm(request.form)
    if request.method == 'POST':
        if form.validate():
            account_email = form.email.data
            user = User.query.filter_by(email=account_email).first_or_404()
            send_email(form.email.data,
                       'Reset Your Password',
                       'email/reset_password.html',
                       user=user,
                       token=user.generate_token())
            flash('We have sent a verification email to ' +
                  account_email +
                  '. Please check it to reset your password.')
    return render_template('auth/forget_password_request.html', form=form)


@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    form = ResetPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        success = User.reset_password(token, form.password1.data)
        if success:
            flash('Reset your password successfully! Please log in again.')
            return redirect(url_for('web.login'))
        else:
            flash('Fail to reset your password.')
    return render_template('auth/forget_password.html', form=form)


@web.route('/change/password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        with db.auto_commit():
            current_user.password = form.new_password1.data
        flash('Update your password successfully!')
        return redirect(url_for('web.personal'))
    return render_template('auth/change_password.html', form=form)


@web.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('web.index'))
