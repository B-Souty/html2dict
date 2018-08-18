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
            table_name = get_text_content(caption)
        elif table_name and not caption_name_overwrite:
            table_name = table_name

        t_body = table.xpath('*//tr') or table.xpath('tr')

        for row in t_body:

            if is_header(row):
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
            except KeyError:
                raise KeyError(
                    f"'{column}' is not a valid header. Valid headers are {self.header_rows}"
                )

        return [row for row in self.data_rows if query in row.values()]


def is_header(row):
        """Check if an html row is a header.

        Args:
            row (HtmlElement): An html row <tr>.

        Returns:
            True if the row is only made of 'header' cells (<th>).

        """

        return all([True if elem.tag == 'th' else False for elem in row.xpath('*')] or False)


def get_text_content(cell):
    """Get the text content of an html cell

    Extract the text content of a cell in a html table. If the cell is part of a
    merged header, join its text with a "/" with the text of the cell below it.

    Args:
        cell (HtmlElement): Html cell <td> or <th>

    Returns:
        str: Text content at the root of an html cell.

    """

    colspan = int(cell.attrib.get('colspan', 1))

    cell_is_header = True if cell.tag == 'th' else False
    cell_text = " ".join(
        [i for i in cell.itertext() if i not in ('\\n',)]).strip() or "n/a"

    if (colspan > 1 or cell.attrib.get('Html2Dict_merged') == "True") and cell_is_header:

        cell.attrib['Html2Dict_merged'] = "True"
        cell.attrib['colspan'] = str(colspan - 1)
        next_cell_below = cell.getparent().getnext()[0]
        cell.getparent().getnext().remove(next_cell_below)

        cell_text = "/".join([
            cell_text,
            get_text_content(cell=next_cell_below)
        ])

        return cell_text

    return cell_text
