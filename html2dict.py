from lxml import html
import requests


class Table(object):
    """Base table object.

    A Table object holds information about a table, including its name,
    headers row and data rows.

    Attributes:
        name (str): Name of the table.
        header_rows (list): A list of headers. If the table doesn't
            contains headers, default ones will be generated.
        data_rows (list): Data rows of your table represented as a list
            of dictionary.
        rows (dict): Headers and data rows together in a dictionary.

    """

    def __init__(self, data_rows: list, header_rows: list, name=None):
        """__init__ method.

        Args:
            name (str, optional): Name of the table. Default to None.
            header_rows (list): A list of headers.
            data_rows (list): Data rows of your table represented as a
                list of dictionary.

        """

        self.name = name
        self.header_rows = header_rows
        self.data_rows = data_rows
        self.rows = {
            "headers": self.header_rows,
            "data": self.data_rows,
        }

    @classmethod
    def from_html_element(cls, table, table_name=None, caption_name_overwrite=False):
        """Classmethod to extract a table from a <table> HTML element.

        This clasmethod is used by the Extractor class to extract the
        tables on a webpage.

        Args:
            table (:obj:`lxml.html.HtmlElement`): A <table> HTML element.
            table_name (str, optional): A table name. Defaults to None.
            caption_name_overwrite (bool, optional): If True, if a table
                name is provided but a table caption is found, the table
                caption will be used as the name instead.

        Returns:
            Table: A Table object

        """

        header_rows = []
        data_rows = []

        if table.xpath('caption'):
            caption = table.xpath('caption')[0]
            table_name = TableExtractor.get_text_content(caption)
        elif table_name and not caption_name_overwrite:
            table_name = table_name

        t_body = table.xpath('*//tr') or table.xpath('tr')

        for row in t_body:

            if TableExtractor.is_header(row):
                header_rows.append(row)
            else:
                data_rows.append(row)

        return cls(
            name=table_name,
            data_rows=data_rows,
            header_rows=header_rows,
        )

    def search(self, query, column=False):
        """Search a value in your data rows.

        Search if a value is present anywhere in your table or in a
        specific column.

        Args:
            query : Value to search
            column (str, optional): Column name. Search only in this
                column. Default to None.

        Returns:
            list: Rows containing the searched value.

        """

        if column:

            try:
                return [row for row in self.data_rows if query == row[column]]
            except KeyError as e:
                raise KeyError(
                    f"'{column}' is not a valid header. Valid headers are {self.header_rows}"
                )

        return [row for row in self.data_rows if query in row.values()]


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

    @staticmethod
    def is_header(row):
        """Check if an html row is a header.

        Args:
            row (HtmlElement): An html row <tr>.

        Returns:
            True if the row is only made of 'header' cells (<th>).

        """

        if not row.xpath('*'):
            return False

        for elem in row.xpath('*'):

            if not elem.tag == 'th':
                return False

        return True

    @staticmethod
    def get_text_content(cell, is_header=False):
        """Get the text content of an html cell

        Extract the text content of a cell in a html table. If the cell is part of a
        merged header, join its text with a "/" with the text of the cell below it.

        Args:
            cell (HtmlElement): Html cell <td> or <th>
            is_header (bool, optional): Is the cell a header. Default to False.

        Returns:
            str: Text content at the root of an html cell.

        """
        # base case
        colspan = int(cell.attrib.get('colspan', 1))
        # is_header = True if cell.tag == 'th' else False
        if (colspan > 1 or cell.attrib.get('Html2Dict_merged') == "True") and is_header:
            cell.attrib['Html2Dict_merged'] = "True"
            cell.attrib['colspan'] = str(colspan - 1)
            next_cell_below = cell.getparent().getnext()[0]
            cell.getparent().getnext().remove(next_cell_below)
            cell_text = " ".join(
                [i for i in cell.itertext() if i not in ('\\n',)]).strip() or "n/a"
            cell_text = "/".join([
                cell_text,
                TableExtractor.get_text_content(cell=next_cell_below, is_header=True)
            ])
            return cell_text
        return " ".join([i for i in cell.itertext() if i not in ('\\n',)]).strip() or "n/a"


class BasicTableExtractor(TableExtractor):
    """Basic tables extractor.

    Attributes:
        html_string (str): String representation of an html.
        url (str): Url of the website you are parsing
        raw_tables (:obj:`dict` of :obj: `Table`): dict of all the tables
            present on the page as raw HTML data and headers (<td> & <th>).
        basic_tables (:obj:`dict` of :obj:`Table`): dict of all the tables
            present on the page as plaintext.
        _tree (:obj:`HtmlElement`): Html tree from the root of the
            provided html_string.
        _table_presents (:obj:`list` of :obj:`dict`): List of tables
            present in the html_string as html element <table>.

    """

    def __init__(self, html_string, url=None):
        """__init_ method.

        Args:
            html_string (str): String representation of an html.
            url (str, optional): Url of the website you are parsing.

        """

        super(BasicTableExtractor, self).__init__(html_string, url)
        self.basic_tables = self.extract_basic_tables()

    def basic_table_parser(self, table: Table):
        """ Transform a raw table to a slightly more advanced table.

        Take a Table object containing raw HTML elements and extract
        basic text data from it.

        Args:
            table (:obj:`Table`): A Table object containing data as HTML
                elements.

        Returns:
            Table: A new Table object with its data represented in
                plaintext.

        """
        header_rows = table.header_rows
        data_rows = table.data_rows
        tmp_header_rows = []
        tmp_data_rows = []

        for row in header_rows + data_rows:

            tmp_row = []
            for cell in row:

                colspan = int(cell.attrib.get('colspan', 1))
                for _ in range(colspan):

                    if row in header_rows:
                        cell_text = self.get_text_content(cell=cell, is_header=True)
                    else:
                        cell_text = self.get_text_content(cell=cell)

                    tmp_row.append(cell_text)

            if row in header_rows:
                tmp_header_rows.append(tmp_row)
            else:
                tmp_data_rows.append(tmp_row)

        if not tmp_header_rows:

            tmp_data_rows = [
                {f"col_{ind}": item for ind, item in enumerate(row)}
                for row in tmp_data_rows
            ]
            tmp_header_rows = sorted(
                {header for row in tmp_data_rows for header in row}
            )

        else:
            tmp_data_rows = [
                dict(zip(tmp_header_rows[0], row))
                for row in tmp_data_rows
            ]

        return Table(data_rows=tmp_data_rows, header_rows=tmp_header_rows)

    def extract_basic_tables(self):
        """Basic tables parser.

        Loop over the extracted raw_tables and pass them through the
        basic_table_parser.

        Returns:
            dict: All the tables found in the html string as a dictionary
                of Table object with data and headers as plaintext.

        """

        my_basic_tables = {}
        for my_table in self.raw_tables:
            try:
                basic_table = self.basic_table_parser(self.raw_tables[my_table])
            except Exception as e:
                error = """
                    An error occured with {0}:
                    {1}
                    *****************
                    Proceeding with next table
                """.format(my_table, e)
                print(error)
                continue

            my_basic_tables[my_table] = basic_table

        return my_basic_tables


class RichTableExtractor(TableExtractor):
    """ Rich tables extractor.

    Notes:
        This class is not implemented yet but I am working on it.
        The goal of it is to return more than just plaintext data.
        For example if a cell contains an HTML list <li>, I should
        retrieve it as a Python list or if a cell has a link, I should
        retrieve something like [some_text](my_link).

    """

    def __init__(self):
        raise NotImplementedError("Placeholder class. Feature coming soon..")


if __name__ == '__main__':
    pass
