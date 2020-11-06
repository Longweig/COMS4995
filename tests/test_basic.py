# -*- coding:utf-8 -*-
# @author: lw_guo
# @time: 2020/10/13
import pytest


@pytest.mark.options(debug=False)
def test_app(app):
    app.config.update({'TESTING': True})
    assert app.testing
    assert not app.debug, 'Ensure the app not in debug mode'


def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello, World!'


def test_app(client):
     res = client.get('/')
     assert res.status_code == 200
