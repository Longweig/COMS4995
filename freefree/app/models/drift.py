# -*- coding:utf-8 -*-
# @author: lw_guo
# @time: 2020/12/9
from ..libs.enums import PendingStatus
from ..models.base import Base
from sqlalchemy import Column, Integer, String, SmallInteger


class Drift(Base):
    id = Column(Integer, primary_key=True)

    # shipping info
    recipient_name = Column(String(20), nullable=False)
    address = Column(String(100), nullable=False)
    message = Column(String(200))
    mobile = Column(String(20), nullable=False)

    # book info
    isbn = Column(String(13))
    book_tile = Column(String(50))
    book_author = Column(String(30))
    book_img = Column(String(50))

    # requester info
    requester_id = Column(Integer)
    requester_nickname = Column(String(20))

    # giver info
    gifter_id = Column(Integer)
    gift_id = Column(Integer)
    gifter_nickname = Column(String(20))

    _pending = Column('pending', SmallInteger, default=1)

    @property
    def pending(self):
        return PendingStatus(self._pending)

    @pending.setter
    def pending(self, status):
        self._pending = status.value
