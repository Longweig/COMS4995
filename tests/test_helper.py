# -*- coding:utf-8 -*-
# @author: lw_guo
# @time: 2020/10/13
import pytest
from freefree.app.libs.helper import is_isbn_or_key
from freefree.app.libs.http_helper import HTTP
from freefree.app.libs.enums import PendingStatus
import requests


@pytest.mark.parametrize("test_input,expected",
                         [("978-0439708180", 'isbn'),
                          ('0439064872', 'isbn'),
                          ('Harry Potter', 'key')])
def test_is_key_or_isbn(test_input, expected):
    assert is_isbn_or_key(test_input) == expected


def test_http_helper():
    success_url = 'https://api.github.com/events'
    fail_url = 'https://www.baidu.com/2'
    success_res = HTTP.get(success_url)
    fail_res = HTTP.get(fail_url, return_json=False)
    assert success_res
    assert fail_res == ''


def test_enums():
    status = [PendingStatus.WAITING, PendingStatus.SUCCESS,
              PendingStatus.REJECT, PendingStatus.WITHDRAW]
    key = ['requester', 'gifter']
    for sta in status:
        for k in key:
            assert PendingStatus.pending_str(sta, k)


def test_external_api():
    api1 = 'https://www.googleapis.com/books/v1/volumes?q={}+isbn'
    response = requests.get(api1.format(9780345525567))
    res = response.json()
    assert response.status_code == 200
    assert res['totalItems'] > 0

    api2 = 'https://www.googleapis.com/books/v1/volumes?q={}'
    response = requests.get(api2.format('Harry Potter'))
    res = response.json()
    assert response.status_code == 200
    assert res['totalItems'] > 0
