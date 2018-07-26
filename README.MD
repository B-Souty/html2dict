#### ⚠️Warning: This script is not ready for production use.⚠️
*Not all tables are parseable yet. Please refer to the "Capabilities" section for a list of supported table types.*

# Html2Dict

Simple html tables extractor.

## Prerequisite

* Python 3.6+
* Python module:
  * [lxml](https://lxml.de/)
  
## Installing

1. `pip install html2dict`

## Capabilities

List of table types currently supported:
  * Basic table without headers (returns a tuple of rows as simple list)
  * Basic table with headers (returns a tuple of dictionaries)
  * Complex tables with merged headers (returns a tuple of dictionaries)

List of table types **not** currently supported:
  * Any tables embedded in iframes.
  * Tables with vertical headers (scope=“col”)
  * Tables with new header row after first set of data.

This project is still very new, if the type of table you are parsing is not in this, please let me know the outcome.

## Usage

* Start by instantiating the class with an html string. (I used requests in this example but opening an html file would work just fine)
```Python
from html2dict import Html2Dict
import requests

my_website = requests.get(url="https://www.python.org/downloads/release/python-370/")
extractor = Html2Dict(html_string=my_website.text)
``` 

* The object starts with an attribute 'tables' containing all the tables in the html provided as raw html elements.

```python
>>> extractor.tables

...{'table_0': {'data_rows': [<Element tr at 0x1034e1458>,
...                           <Element tr at 0x1034e14a8>,
...                           <Element tr at 0x1034e1598>,
...                           <Element tr at 0x1034e15e8>,
...                           <Element tr at 0x1034e1638>,
...                           <Element tr at 0x1034e1688>,
...                           <Element tr at 0x1034e16d8>,
...                           <Element tr at 0x1034e1728>,
...                           <Element tr at 0x1034e1778>,
...                           <Element tr at 0x1034e17c8>,
...                           <Element tr at 0x1034e1818>],
...             'header_rows': [<Element tr at 0x1034e1548>]}}
```

 * The only table extractor method implemented so far is 'basic_tables'. It returns a dict of table where each table is a tuple of dict if the base table had headers otherwise it is a simple list.  
 
 ```python
>>> extractor.basic_tables()

...{'table_0': ({'Description': 'n/a',
...              'File Size': '22745726',
...              'GPG': 'SIG',
...              'MD5 Sum': '41b6595deb4147a1ed517a7d9a580271',
...              'Operating System': 'Source release',
...              'Version': 'Gzipped source tarball'},
...             {'Description': 'n/a',
...              'File Size': '16922100',
...              'GPG': 'SIG',
...              'MD5 Sum': 'eb8c2a6b1447d50813c02714af4681f3',
...              'Operating System': 'Source release',
...              'Version': 'XZ compressed source tarball'},
...             {'Description': 'for Mac OS X 10.6 and later',
...              'File Size': '34274481',
...              'GPG': 'SIG',
...              'MD5 Sum': 'ca3eb84092d0ff6d02e42f63a734338e',
...              'Operating System': 'Mac OS X',
...              'Version': 'macOS 64-bit/32-bit installer'},
...             {'Description': 'for OS X 10.9 and later',
...              'File Size': '27651276',
...              'GPG': 'SIG',
...              'MD5 Sum': 'ae0717a02efea3b0eb34aadc680dc498',
...              'Operating System': 'Mac OS X',
...              'Version': 'macOS 64-bit installer'},
...             {'Description': 'n/a',
...              'File Size': '8547689',
...              'GPG': 'SIG',
...              'MD5 Sum': '46562af86c2049dd0cc7680348180dca',
...              'Operating System': 'Windows',
...              'Version': 'Windows help file'},
...             {'Description': 'for AMD64/EM64T/x64',
...              'File Size': '6946082',
...              'GPG': 'SIG',
...              'MD5 Sum': 'cb8b4f0d979a36258f73ed541def10a5',
...              'Operating System': 'Windows',
...              'Version': 'Windows x86-64 embeddable zip file'},
...             {'Description': 'for AMD64/EM64T/x64',
...              'File Size': '26262280',
...              'GPG': 'SIG',
...              'MD5 Sum': '531c3fc821ce0a4107b6d2c6a129be3e',
...              'Operating System': 'Windows',
...              'Version': 'Windows x86-64 executable installer'},
...             {'Description': 'for AMD64/EM64T/x64',
...              'File Size': '1327160',
...              'GPG': 'SIG',
...              'MD5 Sum': '3cfdaf4c8d3b0475aaec12ba402d04d2',
...              'Operating System': 'Windows',
...              'Version': 'Windows x86-64 web-based installer'},
...             {'Description': 'n/a',
...              'File Size': '6395982',
...              'GPG': 'SIG',
...              'MD5 Sum': 'ed9a1c028c1e99f5323b9c20723d7d6f',
...              'Operating System': 'Windows',
...              'Version': 'Windows x86 embeddable zip file'},
...             {'Description': 'n/a',
...              'File Size': '25506832',
...              'GPG': 'SIG',
...              'MD5 Sum': 'ebb6444c284c1447e902e87381afeff0',
...              'Operating System': 'Windows',
...              'Version': 'Windows x86 executable installer'},
...             {'Description': 'n/a',
...              'File Size': '1298280',
...              'GPG': 'SIG',
...              'MD5 Sum': '779c4085464eb3ee5b1a4fffd0eabca4',
...              'Operating System': 'Windows',
...              'Version': 'Windows x86 web-based installer'})}

```
