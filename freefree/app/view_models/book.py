# -*- coding:utf-8 -*-
# @author: lw_guo
# @time: 2020/11/5

class BookViewModel:
    def __init__(self, book):
        self.title = book['title']
        self.publisher = book['publisher']
        self.author = ','.join(book['author']),
        self.pages = book['pages'] or '',
        self.price = book['pages'],
        self.summary = book['summary'] or '',
        self.image = book['image']

    @property
    def intro(self):
        intros = filter(lambda x: True if x else False,
                        [self.author, self.publisher, self.price])
        return '/'.join(intros)