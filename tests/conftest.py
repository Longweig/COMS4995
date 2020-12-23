# -*- coding:utf-8 -*-
# @author: lw_guo
# @time: 2020/10/13
import pytest
from tests.myapp import create_app


@pytest.fixture
def app():
    app = create_app()
    app.config.from_pyfile('../freefree/app/setting.py')
    return app


@pytest.fixture()
def client(app):
    return app.test_client()
