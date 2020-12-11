#!/usr/bin/python3
# -*- coding:utf-8 -*-
from flask import Blueprint, render_template

web = Blueprint('web', __name__)


@web.app_errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


from freefree.app.web import book
from freefree.app.web import auth
from freefree.app.web import drift
from freefree.app.web import gift
from freefree.app.web import main
from freefree.app.web import wish
