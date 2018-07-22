from lxml import html


class Html2Dict(object):

    def __init__(self, html_string, url=None):

        self.html_string = html_string
        self.url = url
        self._tree = html.fromstring(self.html_string)
        self._table_presents = self._tree.xpath('//table')
        if not self.url and self._tree.xpath('//link[@rel="canonical"]'):
            self.url = self._tree.xpath('//link[@rel="canonical"]')[0].get('href')
        self.tables = self._extract_tables()

    def _extract_tables(self):

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

        if not row.xpath('*'):
            return False

        for elem in row.xpath('*'):

            if not elem.tag == 'th':
                return False

        return True

    @staticmethod
    def get_text_content(cell, is_header=False):

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

        raise NotImplementedError('This feature is coming soon.')

if __name__ == '__main__':
    pass
