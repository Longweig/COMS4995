# -*- coding:utf-8 -*-
# @author: lw_guo
# @time: 2020/12/2
from freefree.app.view_models.book import BookViewModel


class TradeInfo:
    def __init__(self, items):
        self.total = 0
        self.trades = []
        self.__parse(items)

    def __parse(self, items):
        self.total = len(items)
        self.trades = [self.__map_to_trade(single_item)
                       for single_item in items]

    def __map_to_trade(self, single_item):
        if single_item.create_datetime:
            time = single_item.create_datetime.strftime('%Y-%m-%d')
        else:
            time = 'Unknown'
        return dict(
            user_name=single_item.user.nickname,
            time=time,
            id=single_item.id
        )


class MyTrades:
    def __init__(self, trades_of_mine, trade_count_list):
        self.trades = []
        self.__trades_of_mine = trades_of_mine
        self.__trade_count_list = trade_count_list
        self.trades = self.__parse()

    def __parse(self):
        temp_trades = []
        for trade in self.__trades_of_mine:
            my_trade = self.__matching(trade)
            temp_trades.append(my_trade)
        return temp_trades

    def __matching(self, trade):
        count = 0
        for trade_count in self.__trade_count_list:
            if trade.isbn == trade_count['isbn']:
                count = trade_count['count']
        r = {
            'wishes_count': count,
            'book': BookViewModel(trade.book),
            'id': trade.id
        }

        return r
