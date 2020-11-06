from freefree.app.libs.http_helper import HTTP
from flask import current_app


class Book:
    """Book Response

    :param total: The number of items in http response either by 
        search_by_keyword or search_by_isbn. When it is
        result from search_by_isbn, `total` is 0 if the result
        is null and 1 if the item is found.
    :type total: int
    :param books: A list of possible book records in json format.
    :type books: list
    """

    isbn_url = 'http://t.talelin.com/v2/book/isbn/{}'
    keyword_url = 'http://t.talelin.com/v2/book/search?q={}&count={}&start={}'

    def __init__(self):
        """Constructor method
        """
        self.total = 0
        self.books = []

    def search_by_keyword(self, q, page=1):
        """Get formatted HTTP response by keword `q` and specified page number `page`
        and record results in `books` attribute.

        :param q: Keywords for searching books.
        :type q: string
        :param page: Searched page numbe, defaults to 1. 
        :type page: int
        """
        url = self.keyword_url.format(q, current_app.config['PER_PAGE'],
                                      self.calculate_start(page))
        result = HTTP.get(url)
        self.__fill_collection(result)

    def search_by_isbn(self, isbn):
        """Get formatted HTTP response by isbn number and record it in the `books` attribute.

        :param isbn: The unique ID number in specific format of books used for search. 
        :type isbn: string
        """
        url = self.isbn_url.format(isbn)
        result = HTTP.get(url)
        self.__fill_single(result)

    def __fill_single(self, data):
        """Append the  single record searched by ISBN number 
        in the HTTP response to the `books` attribute. 

        :param data: Results getting from formatted HTTP requests
        :type data: json format records or ''
        """
        if data:
            self.total = 1
            self.books.append(data)

    def __fill_collection(self, data):
        """Append the whole records searched by keywords 
        in the HTTP response to the `books` attribute. 

        :param data: Results getting from formatted HTTP requests
        :type data: json format records or ''
        """
        self.total = data['total']
        self.books = data['books']

    def calculate_start(self, page):
        """Returns an integer representing the `start` fitting in outside API function.
        Calculate the `start` index of the API function parameter by `page` and `PER_PAGE`.

        :param page: Specified page number
        :type page: int
        :return: `start` index
        :rtype: int
        """
        return (page - 1) * current_app.config['PER_PAGE']
