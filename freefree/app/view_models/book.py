class BookViewModel:
    """Book view model which stores book information

    :param book: One piece of possible book records in json format
    :type book: json format
    :param title: book title
    :type title: string
    :param publisher: book publisher
    :type publisher: string
    :param author: book author
    :type author: string
    :param pages: number of book pages
    :type pages: string
    :param price: price of book
    :type price: string
    :param summary: summary of book
    :type summary: string
    :param image: image of book
    :type image: string
    """
    def __init__(self, book):
        """Constructor method"""
        self.title = book['title']
        self.publisher = book['publisher']
        self.author = ','.join(book['author']),
        self.pages = book['pages'] or '',
        self.price = book['price'],
        self.summary = book['summary'] or '',
        self.image = book['image']

    @property
    def intro(self):
        """Return a string of short information of book like 'author/publisher/price'
        or 'author/price' when publisher is `null` or unknown.

        :return: short information of book
        :rtype: string
        """
        intros = filter(lambda x: True if x else False,
                        [self.author, self.publisher, self.price])
        return '/'.join(intros)


class BookCollection:
    """A collection of `bookviewmodel` objects

    :param total: total number of books
    :total type: int
    :param books: list of bookviewmodel objects
    :type books: list
    :param keyword: keywords for searching the books
    :type keyword: string
    """
    def __init__(self):
        """Constructor method"""
        self.total = 0
        self.books = []
        self.keyword = ''

    def fill(self, book_item, keyword):
        """
        Fill the book_item into a list of `bookviewmodel` objects

        :param book_item: `Book` Object containing book records
        :type book_item: obj
        :param keyword: The keyword used for searching the `book_item`
        :type keyword: string
        """
        self.total = book_item.total
        self.keyword = keyword
        self.books = [BookViewModel(book) for book in book_item.books]
