# -*- coding:utf-8 -*-
# @author: lw_guo
# @time: 2020/11/19
from math import floor

from flask import current_app
from sqlalchemy import Column, Integer, String, Boolean, Float
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from freefree.app.libs.helper import is_isbn_or_key
from freefree.app.models.base import Base, db
from freefree.app import login_manager
from freefree.app.libs.enums import PendingStatus
from freefree.app.models.drift import Drift
from freefree.app.spider.book_item import Book
from freefree.app.models.gift import Gift
from freefree.app.models.wish import Wish


class User(Base, UserMixin):
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True)
    _password = Column('password', String(128), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self._password, raw)

    def can_save_to_list(self, isbn):
        if is_isbn_or_key(isbn) != 'isbn':
            return False
        book_item = Book()
        book_item.search_by_isbn(isbn)
        if not book_item.first:
            return False

        gifting = Gift.query.filter_by(uid=self.id, isbn=isbn,
                                       launched=False).first()
        wishing = Wish.query.filter_by(uid=self.id, isbn=isbn,
                                       launched=False).first()
        if not gifting and not wishing:
            return True
        else:
            return False

    def generate_token(self, expiration=600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except Exception:
            return False
        uid = data.get('id')
        with db.auto_commit():
            user = User.query.get(uid)
            user.password = new_password
        return True

    def can_drift(self):
        if self.beans < 1:
            return False

        success_gifts_count = Gift.query.filter_by(
            uid=self.id,
            launched=True).count()
        success_receive_count = Drift.query.filter_by(
            requester_id=self.id,
            pending=PendingStatus.SUCCESS).count()

        if floor(success_receive_count / 2) <= success_gifts_count:
            return True
        else:
            return False

    @property
    def summary(self):
        return dict(
            nickname=self.nickname,
            beans=self.beans,
            email=self.email,
            send_recieve=
            str(self.send_counter) + '/' + str(self.receive_counter))


@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))
