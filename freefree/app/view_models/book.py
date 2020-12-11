class BookViewModel:
    """Book view model to store book information

    :param title: book title
    :type title: string
    :param publisher: publisher of book
    :type publisher: string
    :param author: book author
    :type author: string
    :param pages: number of pages of book
    :type pages: string
    :param price: price of book
    :type price: string
    :param summary: summary of book
    :type summary: string
    :param image: images of book
    :type image: string
    """

    def __init__(self, book):
        self.title = book['title']
        self.publisher = book['publisher']
        self.author = '、'.join(book['author'])
        self.pages = book['pages'] or ''
        self.price = book['price']
        self.isbn = book['isbn']
        self.summary = book['summary'] or ''
        self.image = book['image']
        self.pubdate = book['pubdate']
        self.binding = book['binding']

    @property
    def intro(self):
        """
        Get a short introduction of books in format of
        'author/publisher/price' or 'author/price' when
        `publisher` is `null` or unknown.

        :return: A string of short introduction to book
        :rtype: string
        """
        intros = filter(lambda x: True if x else False,
                        [self.author, self.publisher, self.price])

        return ' / '.join(intros)


class BookCollection:
    """A collection of `BookViewModel` objects
    based on a specific keywords

    :param total: the total number of `BookViewModel` objects in
    the collection
    :type total: int
    :param books: list of `BookViewModel` objects
    :type books: list
    :param keyword: keyword used for
    searching for such book collection
    """

    def __init__(self):
        """Constructor Method"""
        self.total = 0
        self.books = []
        self.keyword = ''

    def fill(self, book_item, keyword):
        """Fill the `BookViewModel` objects into
        `books` attribute

        :param book_item: `Book` object returned by getting HTTP response
        :type book_item: obj
        :param keyword: Query keywords for searching `book_item`
        :type keyword: string
        """
        self.total = book_item.total
        self.keyword = keyword
        self.books = [BookViewModel(book) for book in book_item.books]


class _BookViewModel:
    @classmethod
    def package_single(cls, data, keyword):
        returned = {
            'books': [],
            'total': 0,
            'keyword': keyword
        }
        if data:
            returned['total'] = 1
            returned['books'] = [cls.__cut_book_data(data)]
        return returned

    @classmethod
    def package_collection(cls, data, keyword):
        returned = {
            'books': [],
            'total': 0,
            'keyword': keyword
        }
        if data:
            returned['total'] = data['total']
            returned['books'] = [cls.__cut_book_data(book)
                                 for book in data['books']]
        return returned

    @classmethod
    def __cut_book_data(cls, data):
        book = {
            'title': data['title'],
            'publisher': data['publisher'],
            'pages': data['pages'] or '',
            'author': '、'.join(data['author']),
            'price': data['price'],
            'summary': data['summary'] or '',
            'image': data['image']
        }
        return book

    @classmethod
    def __cut_books_data(cls, data):
        books = []
        for book in data['books']:
            r = {
                'title': book['title'],
                'publisher': book['publisher'],
                'pages': book['pages'],
                'author': '****'.join(book['author']),
                'price': book['price'],
                'summary': book['summary'],
                'image': book['image']
            }
            books.append(r)
        return books
