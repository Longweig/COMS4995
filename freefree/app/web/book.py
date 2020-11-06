from flask import jsonify, request, flash, render_template
from app.forms.book import SearchForm
from app.spider.book_item import Book
from app.view_models.book import BookViewModel, BookCollection
from app.web import web
import json
from app.libs.helper import is_isbn_or_key


@web.route('/')
def home():
    return 'OK', 200


@web.route('/book/search')
def search():
    form = SearchForm(request.args)
    books = BookCollection()

    if form.validate():
        q = form.q.data.strip()
        page = form.page.data
        isbn_or_key = is_isbn_or_key(q)
        book = Book()

        if isbn_or_key == 'isbn':
            book.search_by_isbn(q)
        else:
            book.search_by_keyword(q, page)

        books.fill(book, q)

    else:
        flash('Keywords are not legal! Please try checking your spelling.')
        # return jsonify(form.errors)
    return render_template('search_result.html', books=books, form=form)


@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    pass
