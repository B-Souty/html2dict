from lxml import html
import requests
from html2dict.resources import *


__all__ = [
    'TableExtractor',
    'Table',
    'get_text_content',
    'is_header'
]

class TableExtractor(object):
    """Html to dictionaries extractor class

    This is the skeleton Extractor class.

    Attributes:
        html_string (str): String representation of an html.
        url (str): Url of the website you are parsing
        raw_tables (:obj:`dict` of :obj: `Table`): dict of all the tables
            present on the page as raw HTML data and headers (<td> & <th>).
        _tree (:obj:`HtmlElement`): Html tree from the root of the
            provided html_string.
        _table_presents (:obj:`list` of :obj:`dict`): List of tables
            present in the html_string as html element <table>.

    """

    def __init__(self, html_string: str, url=None):
        """__init__ method.

        Args:
            html_string (str): String representation of an html.
            url (str, optional): Url of the website you are parsing.

        Notes:
            It is not recommended to instantiate a class manually. Use
            instead one of the clasmethod provided.

        """

        self.html_string = html_string
        self._tree = html.fromstring(self.html_string)
        self.url = url
        if not self.url and self._tree.xpath('//link[@rel="canonical"]'):
            self.url = self._tree.xpath('//link[@rel="canonical"]')[0].get('href')
        self._table_presents = self._tree.xpath('//table')
        self.raw_tables = self._extract_raw_tables()

    def _extract_raw_tables(self):
        """Hidden method to initialize the self.raw_tables attribute.

        Iterates over the tables in self._table_presents and returns a
        dict of the extracted tables.

        Returns:
            dict: All the tables found in the html string as a dictionary
                of Table object with raw HTML elements for data and
                headers.

        """

        tables = {}

        for ind_table, table in enumerate(self._table_presents):
            my_table = Table.from_html_element(
                table=table,
                table_name=f"table_{ind_table}",
                caption_name_overwrite=True,
            )

            tables[my_table.name] = my_table

        return tables

    @classmethod
    def from_html_string(cls, html_string, url=None):
        """Instantiate an object from an html string.

        Args:
            html_string (str): String representation of an html
            url (str, optional): Url of the website the string is coming
                from. Default to None

        Returns:
            TableExtractor: The newly created TableExtractor

        """

        return cls(html_string=html_string, url=url)

    @classmethod
    def from_html_file(cls, html_file, url=None):
        """Instantiate an object from an html file.

        Args:
            html_file (str): relative filepath to an html file.
            url (str, optional): Url of the website the file is coming
                from. Default to None.

        Returns:
            TableExtractor: The newly created TableExtractor

        """

        with open(html_file, 'r') as infile:
            html_string = infile.read()

        return cls(html_string=html_string, url=url)

    @classmethod
    def from_url(cls, url, **kwargs):
        """Instantiate an object from a url.

        Args:
            url (str): Url of the website you are parsing.

        Returns:
            TableExtractor: The newly created TableExtractor

        """

        html_string = requests.get(url=url, **kwargs).text
        return cls(html_string=html_string, url=url)

