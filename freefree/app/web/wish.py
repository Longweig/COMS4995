from . import web


@web.route('/my/wish')
def my_wish():
    pass


@web.route('/wish/book/<isbn>')
def save_to_wish(isbn):
    pass