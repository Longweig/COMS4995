# -*- coding:utf-8 -*-
# @author: lw_guo
# @time: 2020/10/13
from freefree.app.spider.book_item import Book
from flask import Flask
from tests.myapp import create_app


def test_seacrh_by_isbn():
    isbn_found = '9787501524044'
    isbn_not_found = '123456'
    b1 = Book()
    b2 = Book()
    b1.search_by_isbn(isbn_found)
    b2.search_by_isbn(isbn_not_found)
    assert b1.total == 1
    assert b2.books[0]['msg'] == 'book not found'


def test_seach_by_key():
    key_found = 'Machine Learning'
    key_not_found = 'Today'
    test_app = create_app('../freefree/app/setting.py')
    ctx = test_app.app_context()
    ctx.push()
    b1 = Book()
    b2 = Book()
    with ctx:
        b1.search_by_keyword(q=key_found, page=1)
        b2.search_by_keyword(q=key_not_found, page=1)
    assert b1.total >= 1
    assert b2.total == 0
