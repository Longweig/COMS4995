# -*- coding:utf-8 -*-
# @author: lw_guo
# @time: 2020/10/13

from flask import jsonify
from book_item import Book
from . import web
from helper import is_isbn_or_key

@web.route('/')
def home():
    return 'OK', 200


@web.route('/book/search/<q>/<page>')
def search(q, page):
    isbn_or_key = is_isbn_or_key(q)
    if isbn_or_key == 'isbn':
        result = Book.search_by_isbn(q)
    else:
        result = Book.search_by_keyword(q)

    return jsonify(result)