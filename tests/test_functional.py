# -*- coding:utf-8 -*-
# @author: lw_guo
# @time: 2020/10/13
from freefree.app.spider.book_item import Book
from freefree.app.view_models.book import BookViewModel, BookCollection
from freefree.app.view_models.trade import TradeInfo, MyTrades
from freefree.app.view_models.drift import DriftViewModel, DriftCollection


def test_book_item_class():
    book = Book()
    assert book.total == 0
    assert len(book.books) == 0


def test_search_by_isbn(app):
    isbn_found = '9780262337373'
    isbn_not_found = '1231231231231'
    b1 = Book()
    b2 = Book()
    b1.search_by_isbn(isbn_found)
    b2.search_by_isbn(isbn_not_found)
    isbn_b1 = [item['identifier']
               for item in b1.books[0]['volumeInfo']['industryIdentifiers']]
    isbn_b2 = [item['identifier']
               for item in b2.books[0]['volumeInfo']['industryIdentifiers']]
    is_in = isbn_found in isbn_b1
    not_in = isbn_not_found in isbn_b2
    assert is_in
    assert not not_in


def test_search_by_key(app):
    key_found = 'Machine Learning'
    key_not_found = '   '
    b1 = Book()
    b2 = Book()
    with app.app_context():
        b1.search_by_keyword(q=key_found)
        b2.search_by_keyword(q=key_not_found)
    assert b1.total > 0
    assert b2.total == 0


def test_book_view_model(app):
    book = Book()
    key_found = 'Harry Potter'
    with app.app_context():
        book.search_by_keyword(key_found)
    book_view_models = BookCollection()
    book_view_models.fill(book, key_found)
    assert book_view_models.total > 0
    assert book_view_models.keyword == 'Harry Potter'
    assert len(book_view_models.books) > 0
    assert book_view_models.total == book.total


def test_book_model():
    pass


def test_drift_model():
    pass
