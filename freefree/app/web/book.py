from flask import request, flash, render_template
from flask_login import current_user

from freefree.app.forms.book import SearchForm
from freefree.app.models.gift import Gift
from freefree.app.models.wish import Wish
from freefree.app.spider.book_item import Book
from freefree.app.view_models.book import BookCollection, BookViewModel
from freefree.app.view_models.trade import TradeInfo
from freefree.app.web import web
from freefree.app.libs.helper import is_isbn_or_key


@web.route('/book/search')
def search():
    form = SearchForm(request.args)
    books = BookCollection()

    if form.validate():
        q = form.q.data.strip()
        # page = form.page.data
        isbn_or_key = is_isbn_or_key(q)
        book = Book()

        if isbn_or_key == 'isbn':
            book.search_by_isbn(q)
        else:
            # book.search_by_keyword(q, page)
            book.search_by_keyword(q)

        books.fill(book, q)

    else:
        flash('Keywords are not legal! Please check your spelling.')
        # return jsonify(form.errors)
    return render_template('search_result.html', books=books, form=form)


@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    has_in_gifts = False
    has_in_wishes = False

    # get book info details
    book_item = Book()
    book_item.search_by_isbn(isbn)
    book = BookViewModel(book_item.first)

    if current_user.is_authenticated:
        if Gift.query.filter_by(uid=current_user.id,
                                isbn=isbn,
                                launched=False).first():
            has_in_gifts = True
        if Wish.query.filter_by(uid=current_user.id,
                                isbn=isbn,
                                launched=False).first():
            has_in_wishes = True

    trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()
    trade_wishes = Wish.query.filter_by(isbn=isbn, launched=False).all()

    trade_gifts_model = TradeInfo(trade_gifts)
    trade_wishes_model = TradeInfo(trade_wishes)

    return render_template('book_detail.html',
                           book=book,
                           wishes=trade_wishes_model,
                           gifts=trade_gifts_model,
                           has_in_gifts=has_in_gifts,
                           has_in_wishes=has_in_wishes)
