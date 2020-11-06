from flask import request, flash, render_template
from freefree.app.forms.book import SearchForm
from freefree.app.spider.book_item import Book
from freefree.app.view_models.book import BookCollection
from freefree.app.web import web
from freefree.app.libs.helper import is_isbn_or_key


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
