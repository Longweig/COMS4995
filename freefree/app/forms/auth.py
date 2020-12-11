# -*- coding:utf-8 -*-
# @author: lw_guo
# @time: 2020/12/1
from wtforms import Form, StringField, PasswordField
from wtforms.validators import Length, DataRequired, Email, \
    ValidationError, EqualTo
from freefree.app.models.user import User


class RegisterForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64),
                                    Email(message='Email address is invalid')])

    password = PasswordField(validators=[
        DataRequired(
            message='Password is required. Please enter your password.'),
        Length(6, 32)
    ])

    nickname = StringField(validators=[
        DataRequired(),
        Length(2, 10, message='Nickname requires among 2-20 characters')
    ])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('This email address has been registered')

    def validate_nickname(self, field):
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError(
                'This nickname has existed. Please try another name.')


class LoginForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64),
                                    Email(message='Email address is invalid')])

    password = PasswordField(validators=[
        DataRequired(
            message='Password is required. ''Please enter your password.'),
        Length(6, 32)
    ])


class EmailForm(Form):
    email = StringField(validators=[
        DataRequired(),
        Length(5, 64),
        Email(message="Illegal email address! Please check again.")])


class ResetPasswordForm(Form):
    password1 = PasswordField(validators=[
        DataRequired(),
        Length(6, 32,
               message="Password should be between 6 and 32 characters."),
        EqualTo('password2',
                message="Those passwords didn't match. Try again.")])
    password2 = PasswordField(validators=[
        DataRequired(),
        Length(6, 32)
    ])


class ChangePasswordForm(Form):
    old_password = PasswordField(validators=[DataRequired()])
    new_password1 = PasswordField(validators=[
        DataRequired(), Length(6, 32, message='密码长度至少需要在6到32个字符之间'),
        EqualTo('new_password2', message='两次输入的密码不一致')])
    new_password2 = PasswordField(validators=[DataRequired()])
