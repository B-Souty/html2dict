from html2dict.extractors import BasicTableExtractor
import subprocess
import json
import os


TEST_DATA_FOLDER = "tests"
TEST_HTML_FILE = os.path.join(TEST_DATA_FOLDER, "test_tables.html")
TEST_HTML_STRING = open(TEST_HTML_FILE, 'r').read()

SIMPLE_SERVER = os.path.join(TEST_DATA_FOLDER, 'simple_server.py')
subprocess.Popen([SIMPLE_SERVER, TEST_HTML_FILE])

VALIDATION_FILE = os.path.join(TEST_DATA_FOLDER, 'test_data.json')
VALIDATION_DATA = json.load(open(VALIDATION_FILE, 'r'))


def test_basic_table_from_string():

    test_html = BasicTableExtractor.from_html_string(TEST_HTML_STRING)
    data_rows = [test_html.basic_tables[table].data_rows for table in test_html.basic_tables]

    assert data_rows == VALIDATION_DATA


def test_basic_table_from_file():

    test_html = BasicTableExtractor.from_html_file(TEST_HTML_FILE)
    data_rows = [test_html.basic_tables[table].data_rows for table in test_html.basic_tables]

    assert data_rows == VALIDATION_DATA


def test_basic_table_from_url():

    test_html = BasicTableExtractor.from_url(url="http://127.0.0.1:8081")
    data_rows = [test_html.basic_tables[table].data_rows for table in test_html.basic_tables]

    assert data_rows == VALIDATION_DATA
