# -*- coding:utf-8 -*-
# @author: lw_guo
# @time: 2020/12/3

'''
class MyWishes:
    def __init__(self, gifts_of_mine, wish_count_list):
        self.gifts = []
        self.__gifts_of_mine = gifts_of_mine
        self.__wish_count_list = wish_count_list

        self.gifts = self.__parse()
        pass

    def __parse(self):
        temp_gitfs = []
        for gift in self.__gifts_of_mine:
            my_gift = self.__mathcing(gift)
            temp_gitfs.append(my_gift)
        return temp_gitfs

    def __matching(self, gift):
        count = 0
        for wish_count in self.__wish_count_list:
            if gift.isbn == wish_count['isbn']:
                count = wish_count['count']
        r = {
            'wishes_count': count,
            'book': BookViewModel(gift.book_model),
            'id': gift.id
        }

        return r
'''
