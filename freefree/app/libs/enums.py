# -*- coding:utf-8 -*-
# @author: lw_guo
# @time: 2020/12/9

from enum import Enum


class PendingStatus(Enum):
    WAITING = 1
    SUCCESS = 2
    REJECT = 3
    WITHDRAW = 4

    @classmethod
    def pending_str(cls, status, key):
        key_map = {
            cls.WAITING: {
                'requester': 'Waiting for shipping to you',
                'gifter': 'Waiting for shipping from you'
            },
            cls.REJECT: {
                'requester': 'Rejected by the owner',
                'gifter': 'Have Rejected'
            },
            cls.WITHDRAW: {
                'requester': 'Have withdrawn',
                'gifter': 'Withdrawn by the owner'
            },
            cls.SUCCESS: {
                'requester': 'Shipped by the owner',
                'gifter': 'Have shipped from you. Order complete.'
            }
        }
        return key_map[status][key]
