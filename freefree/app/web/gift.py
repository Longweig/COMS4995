from . import web
from flask_login import login_required, current_user
from freefree.app.models.base import db
from ..libs.enums import PendingStatus
from ..models.drift import Drift
from ..models.gift import Gift
from flask import current_app, flash, redirect, url_for, render_template

from ..view_models.trade import MyTrades


@web.route('/my/gifts')
@login_required
def my_gifts():
    uid = current_user.id
    gifts_of_mine = Gift.get_user_gifts(uid)
    isbn_list = [gift.isbn for gift in gifts_of_mine]
    wish_count_list = Gift.get_wish_counts(isbn_list)
    view_model = MyTrades(gifts_of_mine, wish_count_list)
    return render_template('my_gifts.html', gifts=view_model.trades)


@web.route('/gifts/book/<isbn>')
@login_required
def save_to_gifts(isbn):
    if current_user.can_save_to_list(isbn):
        with db.auto_commit():
            gift = Gift()
            gift.isbn = isbn
            gift.uid = current_user.id
            current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']
            db.session.add(gift)
    else:
        flash("This item has been added to your wishlist or giving list."
              "Please do not submit duplicate items!")
    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/gifts/<gid>/withdraw')
@login_required
def withdraw_from_gifts(gid):
    gift = Gift.query.filter_by(id=gid, launched=False).first_or_404()
    drift = Drift.query.filter_by(
        gift_id=gid, pending=PendingStatus.WAITING).first()
    if drift:
        flash('This gift is in transaction now. '
        'Please complete this order first.')
    else:
        with db.auto_commit():
            current_user.beans -= current_app.config['BEANS_UPLOAD_ONE_BOOK']
            gift.delete()
    return redirect(url_for('web.my_gifts'))
