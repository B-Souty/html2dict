from lxml import html


class Html2Dict(object):
    """Html to dictionaries extractor class

    A simple html tables extractor.

    Args:
        html_string (str): String representation of an html.
        url (str): Url of the website you are parsing

    Attributes:
        html_string (str): String representation of an html.
        url (str): Url of the website you are parsing
        _tree (HtmlElement): Html tree from the root of the provided html_string.
        _table_presents (:obj:`list` of :obj:`dict`): List of tables present in the
            html_string as html element.
        tables (dict): dict of all the table present on the page (structure in Notes).

    Notes:
        Structure of a 'tables' dict:
            dict(
                table_n: dict(
                    header_rows: list(
                        header_row (:obj:`HtmlElement`),
                    ),
                    data_rows: list(
                        data_row (:obj:`HtmlElement`),
                    )
                )
            )

    """

    def __init__(self, html_string, url=None):

        self.html_string = html_string
        self.url = url
        self._tree = html.fromstring(self.html_string)
        self._table_presents = self._tree.xpath('//table')
        if not self.url and self._tree.xpath('//link[@rel="canonical"]'):
            self.url = self._tree.xpath('//link[@rel="canonical"]')[0].get('href')
        self.tables = self._extract_tables()

    def _extract_tables(self):
        """Hidden method to initialize the self.tables attribute.

        Iterates over the tables in self._table_presents and returns a dict of
        the extracted header and data rows for each tables.

        Returns:
            tables (dict): this populate the tables attribute. For the structure please

        """

        tables = {}

        for ind_table, table in enumerate(self._table_presents):

            my_header_rows = []
            my_data_rows = []
            t_body = table.xpath('*//tr') or table.xpath('tr')

            for row in t_body:

                if Html2Dict.is_header(row):
                    my_header_rows.append(row)
                else:
                    my_data_rows.append(row)

            tables["table_{}".format(ind_table)] = {
                "header_rows" : my_header_rows,
                "data_rows": my_data_rows,
            }
        return tables

    @staticmethod
    def is_header(row):
        """For a given html row <tr>, returns True if all cells are header cells <th>.

        Args:
            row (HtmlElement): Any html row <tr>.

        Returns:
            bool:

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
            is_header (:obj:`bool`, optional): Is the cell a header. Default to False.

        Returns:
            _ (str): Text contect at the root of an html cell.

        """
        # base case
        colspan = int(cell.attrib.get('colspan', 1))
        if (colspan > 1 or cell.attrib.get('Html2Dict_merged') == "True") and is_header:
                cell.attrib['Html2Dict_merged'] = "True"
                cell.attrib['colspan'] = str(colspan - 1)
                next_cell_below = cell.getparent().getnext()[0]
                cell.getparent().getnext().remove(next_cell_below)
                return " ".join([i for i in cell.itertext() if i not in ('\\n',)]).strip() or "n/a" + "/" + Html2Dict.get_text_content(cell=next_cell_below)
        return " ".join([i for i in cell.itertext() if i not in ('\\n',)]).strip() or "n/a"

    @staticmethod
    def basic_table(table):
        """ Transform a raw table to a slightly more advanced table.

        Take a dict representation of a table with raw html elements as formatted in
        self.tables (c.f. 'Notes' section of the class.) in input and returns a new
        dict representation of it with the text content of those html elements.

        Args:
            table (dict): For the structure, please see the 'Notes' section of the class.

        Returns:
            _ (dict): For the structure, please see the 'Notes' section of this method.

        Notes:
            Structure of the returned dict:
                dict(
                    headers: list(
                        headers (str) or None
                    ),
                    data_rows: list(
                        data_rows (:obj:`list` of :obj:`str`)
                    )
                )

        """
        copy_table = table.copy()
        header_rows = copy_table['header_rows']
        data_rows = copy_table['data_rows']
        tmp_headers = []
        tmp_data_rows = []

        for row in header_rows + data_rows:

            tmp_row = []
            for cell in row:

                colspan = int(cell.attrib.get('colspan', 1))
                for _ in range(colspan):
                    if row in header_rows:
                        cell_text = Html2Dict.get_text_content(cell=cell, is_header=True)
                    else:
                        cell_text = Html2Dict.get_text_content(cell=cell)

                    tmp_row.append(cell_text)
            if row in header_rows:
                tmp_headers.append(tmp_row)
            else:
                tmp_data_rows.append(tmp_row)
        if not tmp_headers:
            tmp_headers = [None]
        return {'headers': tmp_headers[0], 'data_rows': tmp_data_rows}

    def basic_tables(self):
        """The most basic tables parser.

        Returns:
            my_basic_tables (dict): For the structure, please see the 'Notes' section
                of this method.

        Notes:
            Structure of my_basic_tables:
                If headers are found a row is a dict {header: data}. Otherwise a row is
                a list of data.

                dict(
                    table_n: tuple(
                        row (:obj:`dict` or :obj:`list`)
                    )
                )

        """
        my_basic_tables = {}
        for my_table in self.tables:
            try:
                my_table_basic = Html2Dict.basic_table(self.tables[my_table])
            except Exception as e:
                error = """
                    An error occured with {0}:
                    {1}
                    *****************
                    Proceeding with next table
                """.format(my_table, e)
                print(error)
                continue
            headers = my_table_basic.get('headers')
            my_basic_tables[my_table] = tuple(dict(zip(headers, row)) if headers else row for row in my_table_basic.get('data_rows'))

        return my_basic_tables

    def rich_tables(self):
        """Coming soon."""
        raise NotImplementedError('This feature is coming soon.')

if __name__ == '__main__':
    pass
