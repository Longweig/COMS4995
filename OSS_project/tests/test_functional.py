# -*- coding:utf-8 -*-
# @author: lw_guo
# @time: 2020/10/13
from book_item import Book


def test_seacrh_by_isbn():
    isbn_found = '9787501524044'
    isbn_not_found = '123456'
    res1 = Book.search_by_isbn(isbn_found)
    res2 = Book.search_by_isbn(isbn_not_found)
    assert res1['author']
    assert res2['msg'] == 'book not found'


def test_seach_by_key():
    key_found = 'Machine Learning'
    res1 = Book.search_by_keyword(q=key_found)
    key_not_found = 'Today'
    res2 = Book.search_by_keyword(key_not_found)
    assert len(res1['books']) > 0
    assert len(res2['books']) == 0
