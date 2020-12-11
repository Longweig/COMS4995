# -*- coding:utf-8 -*-
# @author: lw_guo
# @time: 2020/10/13

from flask import Flask
from flask_login import LoginManager
from freefree.app.models.book import db
from flask_mail import Mail

login_manager = LoginManager()
mail = Mail()


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')
    register_blueprint(app)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'web.login'
    login_manager.login_message = 'Please log in or sign up first.'

    mail.init_app(app)

    with app.app_context():
        db.create_all()
    return app


def register_blueprint(app):
    from freefree.app.web.book import web
    app.register_blueprint(web)
