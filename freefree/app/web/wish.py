from . import web
from flask_login import login_required, current_user
from freefree.app.models.base import db
from ..models.gift import Gift
from ..models.wish import Wish
from flask import flash, redirect, url_for, render_template
from ..libs.email import send_email
from ..view_models.trade import MyTrades


@web.route('/my/wish')
@login_required
def my_wish():
    uid = current_user.id
    wishes_of_mine = Wish.get_user_wishes(uid)
    isbn_list = [wish.isbn for wish in wishes_of_mine]
    gift_count_list = Wish.get_gift_counts(isbn_list)
    view_model = MyTrades(wishes_of_mine, gift_count_list)
    return render_template('my_wish.html', wishes=view_model.trades)


@web.route('/wish/book/<isbn>')
@login_required
def save_to_wish(isbn):
    if current_user.can_save_to_list(isbn):
        with db.auto_commit():
            wish = Wish()
            wish.isbn = isbn
            wish.uid = current_user.id
            db.session.add(wish)
    else:
        flash("This item has been added to your wishlist or giving list."
              "Please do not submit duplicate items!")
    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/satisfy/wish/<int:wid>')
@login_required
def satisfy_wish(wid):
    wish = Wish.query.get_or_404(wid)
    gift = Gift.query.filter_by(uid=current_user.id, isbn=wish.isbn).first()
    if not gift:
        flash('You have not uploaded this book yet.'
              'Please click to add this book to gift list.')
    else:
        send_email(wish.user.email,
                   'Someone wants to send you a gift',
                   'email/satisify_wish.html',
                   wish=wish,
                   gift=gift)
        flash('Sent email to him/her. '
              'If he/she agrees to accept your gift, '
              'you will receive a drift then.')
    return redirect(url_for('web.book_detail', isbn=wish.isbn))


@web.route('/wish/book/<isbn>/withdraw')
@login_required
def withdraw_from_wish(isbn):
    wish = Wish.query.filter_by(isbn=isbn, launched=False).first_or_404()
    with db.auto_commit():
        wish.delete()
    return redirect(url_for('web.my_wish'))
