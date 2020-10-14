# -*- coding:utf-8 -*-
# @author: lw_guo
# @time: 2020/10/13
import pytest
from flask import Flask
from helper import is_isbn_or_key
from http_helper import HTTP

@pytest.mark.parametrize("test_input,expected",\
                  [("978-0439708180", 'isbn'),\
                   ('0439064872', 'isbn'),\
                   ('Harry Potter', 'key') \
                    ])
def test_is_key_or_isbn(test_input, expected):
    assert is_isbn_or_key(test_input) == expected



def test_http_helper():
    success_url = 'https://api.github.com/events'
    fail_url = 'https://www.baidu.com/2'
    success_res = HTTP.get(success_url)
    fail_res = HTTP.get(fail_url, return_json=False)
    assert success_res
    assert fail_res == ''


