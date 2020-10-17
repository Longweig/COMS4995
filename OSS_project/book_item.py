# -*- coding:utf-8 -*-
# @author: lw_guo
# @time: 2020/10/13
from http_helper import HTTP


class Book:
    isbn_url = 'http://t.yushu.im/v2/book/isbn/{}'
    keyword_url = 'http://t.yushu.im/v2/book/search?q={}&count={}&start={}'

    @classmethod
    def search_by_keyword(cls, q, count=20, start=0):
        url = cls.keyword_url.format(q, count, start)
        result = HTTP.get(url)
        return result

    @classmethod
    def search_by_isbn(cls, isbn):
        url = cls.isbn_url.format(isbn)
        result = HTTP.get(url)
        return result
    
