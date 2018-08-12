from html2dict.base_extractor import *


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

    @staticmethod
    def basic_table_parser(table: Table):
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

                    cell_text = get_text_content(cell=cell)
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
                basic_table = BasicTableExtractor.basic_table_parser(self.raw_tables[my_table])
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
