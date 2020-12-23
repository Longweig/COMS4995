# -*- coding:utf-8 -*-
# @author: lw_guo
# @time: 2020/12/9
import time
from freefree.app.libs.enums import PendingStatus


class DriftCollection:
    def __init__(self, drifts, current_user_id):
        """A collection of `DriftView` objects
        based on a drift record and user id
        :param drifts: the records related to `current_user_id` 
        in the database
        :type drifts: obj
        :param current_user_id: user id linked to drift records
        :type current_user_id: str
        """
        self.data = []
        self.__parse(drifts, current_user_id)

    def __parse(self, drifts, current_user_id):
        for drift in drifts:
            temp = DriftViewModel(drift, current_user_id)
            self.data.append(temp.data)


class DriftViewModel:
    def __init__(self, drift, current_user_id):
        """
        :param drift: the record related to `current_user_id`
        in the database
        :type total: obj
        :param current_user_id: user id linked to drift record
        :type current_user_id: str
        """
        self.data = {}
        self.data = self.__parse(drift, current_user_id)

    @staticmethod
    def requester_or_gifter(drift, current_user_id):
        """
        Based on the drift records confirm an user with \
        `current_user_id` is a requester of a giver of the book.

        :param drift: the record related to `current_user_id`\
        in the database
        :type total: obj
        :param current_user_id: user id linked to drift record
        :type current_user_id: str
        :return: A string of the user identity
        :rtype: string, `requester` or `gifter`
        """
        if drift.requester_id == current_user_id:
            you_are = 'requester'
        else:
            you_are = 'gifter'
        return you_are

    def __parse(self, drift, current_user_id):
        you_are = self.requester_or_gifter(drift, current_user_id)
        pending_status = PendingStatus.pending_str(drift.pending, you_are)
        time_local = time.localtime(drift.create_time)

        r = {
            'you_are': you_are,
            'drift_id': drift.id,
            'book_title': drift.book_tile,
            'book_author': drift.book_author,
            'book_img': drift.book_img,
            'date': time.strftime('%Y-%m-%d', time_local),
            'operator': drift.requester_nickname if you_are != 'requester'
            else drift.gifter_nickname,
            'message': drift.message,
            'address': drift.address,
            'pending_str': pending_status,
            'recipient_name': drift.recipient_name,
            'mobile': drift.mobile,
            'status': drift.pending
        }

        return r
