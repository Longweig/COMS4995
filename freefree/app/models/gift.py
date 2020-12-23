# -*- coding:utf-8 -*-
# @author: lw_guo
# @time: 2020/11/19
from flask import current_app
from sqlalchemy import Column, Integer, Boolean, ForeignKey, String, desc, func
from freefree.app.models.base import Base, db
from sqlalchemy.orm import relationship
from freefree.app.spider.book_item import Book
from freefree.app.view_models.book import BookViewModel


class Gift(Base):
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    isbn = Column(String(15), nullable=False)
    # book = relationship('Book')
    # bid = Column(Integer, ForeignKey('book.id'))
    launched = Column(Boolean, default=False)

    def is_yourself_gift(self, uid):
        """
        Determine if the gift record related to the user with\
        `uid`.

        :param uid: user id
        :type uid: str
        :return: `True` or `False`
        :rtype: Boolean
        """
        return True if self.uid == uid else False

    @classmethod
    def get_user_gifts(cls, uid):
        """
        Get all the gifts records related to the user with\
        `uid`. 

        :param uid: user id
        :type uid: str
        :return: gift records in the database
        :rtype: Obj
        """
        gifts = Gift.query.filter_by(uid=uid, launched=False).order_by(
            desc(Gift.create_time)).all()
        return gifts

    @classmethod
    def get_wish_counts(cls, isbn_list):
        """
        Count the number of the wishes related to the book with\
        isbn numbers included in `isbn_list`.

        :param isbn_list: a list of isbn numbers
        :type isbn_list: list
        :return: a list of the wish counts of the books of each isbn\
        number
        :rtype: list
        """
        count_list = db.session.query(func.count(Wish.id), Wish.isbn).filter(
            Wish.launched == False,
            Wish.isbn.in_(isbn_list),
            Wish.status == 1).group_by(
            Wish.isbn).all()
        count_list = [{'count': w[0], 'isbn': w[1]} for w in count_list]
        return count_list

    @property
    def book(self):
        """
        The information of the books related to the gifts which is returned \
        by the external APIs.

        :return: one piece response in the format of `Book` object
        :rtype: object
        """
        book_model = Book()
        book_model.search_by_isbn(self.isbn)
        return book_model.first

    @property
    def reset_book(self):
        """
        The information of the books related to the gifts which is returned \
        by the external APIs.

        :return: one piece response in the format of `BookViewModel` object
        :rtype: object
        """
        return BookViewModel(self.book)

    @classmethod
    def recent(cls):
        """
        Recent book info of the gifts which are ordered by `create_time`.

        :return: list of records in the format of `Book` object
        :rtype: list
        """
        recent_gift = Gift.query.filter_by(
            launched=False).group_by(
            Gift.isbn).order_by(
            desc(Gift.create_time)).limit(
            current_app.config['RECENT_BOOK_COUNT']).all()
        return recent_gift


from freefree.app.models.wish import Wish
