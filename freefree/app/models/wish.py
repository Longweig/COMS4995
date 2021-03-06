# -*- coding:utf-8 -*-
# @author: lw_guo
# @time: 2020/12/1
from sqlalchemy import Column, Integer, Boolean, ForeignKey, String, desc, func
from freefree.app.models.base import Base, db
from sqlalchemy.orm import relationship
from freefree.app.spider.book_item import Book
from freefree.app.view_models.book import BookViewModel


class Wish(Base):
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    isbn = Column(String(15), nullable=False)
    # book = relationship('Book')
    # bid = Column(Integer, ForeignKey('book.id'))
    launched = Column(Boolean, default=False)

    @classmethod
    def get_user_wishes(cls, uid):
        wishes = Wish.query.filter_by(uid=uid, launched=False).order_by(
            desc(Wish.create_time)).all()
        return wishes

    @classmethod
    def get_gift_counts(cls, isbn_list):
        count_list = db.session.query(func.count(Gift.id), Gift.isbn).filter(
            Gift.launched == False,
            Gift.isbn.in_(isbn_list),
            Gift.status == 1).group_by(
            Gift.isbn).all()
        count_list = [{'count': w[0], 'isbn': w[1]} for w in count_list]
        return count_list

    @property
    def book(self):
        book_model = Book()
        book_model.search_by_isbn(self.isbn)
        return book_model.first

    @property
    def reset_book(self):
        return BookViewModel(self.book)


from freefree.app.models.gift import Gift
