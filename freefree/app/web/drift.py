from flask import flash, redirect, url_for, render_template, request
from flask_login import login_required, current_user
from sqlalchemy import desc, or_

from . import web
from ..forms.book import DriftForm
from ..libs.email import send_email
from ..libs.enums import PendingStatus
from ..models.base import db
from ..models.drift import Drift
from ..models.gift import Gift
from ..models.user import User
from ..models.wish import Wish
from ..view_models.book import BookViewModel
from ..view_models.drift import DriftCollection


@web.route('/drift/<int:gid>', methods=['GET', 'POST'])
@login_required
def send_drift(gid):
    current_gift = Gift.query.get_or_404(gid)
    if current_gift.is_yourself_gift(current_user.id):
        flash("You cannot ask for the book that you owned! Please try again.")
        return redirect(url_for('web.book_detail', isbn=current_gift.isbn))

    can = current_user.can_drift()
    if not can:
        return render_template('not_enough_beans.html',
                               beans=current_user.beans)
    form = DriftForm(request.form)
    if request.method == 'POST' and form.validate():
        save_drift(form, current_gift)
        send_email(current_gift.user.email,
                   'Someone wants your book.',
                   'email/get_gift.html',
                   wisher=current_user,
                   gift=current_gift)
        return redirect(url_for('web.pending'))

    sender = current_gift.user.summary
    return render_template('drift.html', gifter=sender,
                           user_beans=current_user.beans,
                           form=form)


@web.route('/pending')
@login_required
def pending():
    drifts = Drift.query.filter(
        or_(Drift.requester_id == current_user.id,
            Drift.gifter_id == current_user.id)).order_by(
        desc(Drift.create_time)
    ).all()

    views = DriftCollection(drifts, current_user.id)
    return render_template('pending.html', drifts=views.data)


@web.route('/drift/<int:did>/reject')
@login_required
def reject_drift(did):
    with db.auto_commit():
        drift = Drift.query.filter(
            Gift.uid == current_user.id,
            Drift.id == did).first_or_404()

        drift.pending = PendingStatus.REJECT
        requester = User.query.get_or_404(drift.requester_id)
        requester.beans += 1
    return redirect(url_for('web.pending'))


@web.route('/drift/<int:did>/withdraw')
@login_required
def withdraw_drift(did):
    with db.auto_commit():
        drift = Drift.query.filter_by(
            requester_id=current_user.id, id=did).first_or_404()
        drift.pending = PendingStatus.WITHDRAW
        current_user.beans += 1
    return redirect(url_for('web.pending'))


@web.route('/drift/<int:did>/mailed')
@login_required
def mailed_drift(did):
    with db.auto_commit():
        drift = Drift.query.filter_by(
            gifter_id=current_user.id,
            id=did).first_or_404()
        drift.pending = PendingStatus.SUCCESS
        current_user.beans += 1
        gift = Gift.query.filter_by(id=drift.gift_id).first_or_404()
        gift.launched = True
        wish = Wish.query.filter_by(isbn=drift.isbn,
                                    uid=drift.requester_id,
                                    launched=False).first_or_404()
        wish.launched = True
    return redirect(url_for('web.pending'))


def save_drift(drift_form, current_gift):
    with db.auto_commit():
        drift = Drift()
        drift_form.populate_obj(drift)

        drift.gift_id = current_gift.id
        drift.requester_id = current_user.id
        drift.requester_nickname = current_user.nickname
        drift.gifter_nickname = current_gift.user.nickname
        drift.gifter_id = current_gift.user.id
        book = BookViewModel(current_gift.book)
        drift.book_tile = book.title
        drift.book_author = book.author
        drift.book_img = book.image
        drift.isbn = book.isbn

        current_user.beans -= 1

        db.session.add(drift)
