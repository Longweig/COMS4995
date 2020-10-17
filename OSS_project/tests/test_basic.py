# -*- coding:utf-8 -*-
# @author: lw_guo
# @time: 2020/10/13

def test_config(app):
    assert not app.testing
    assert app.debug
    app.config.update({'TESTING': True})
    assert app.testing


def test_app(client):
    res = client.get('/')
    assert res.status_code == 200
