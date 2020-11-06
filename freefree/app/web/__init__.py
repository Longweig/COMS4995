#!/usr/bin/python3
# -*- coding:utf-8 -*-
from flask import Blueprint

web = Blueprint('web', __name__)

from freefree.app.web import book
from freefree.app.web import auth
from freefree.app.web import drift
from freefree.app.web import gift
from freefree.app.web import main
from freefree.app.web import wish
