from setuptools import setup

NAME = 'html2dict'
DESCRIPTION = 'Simple html tables extractor.'
URL = 'https://github.com/B-Souty/html2dict'
EMAIL = 'benjamin.souty@gmail.com'
AUTHOR = 'B-Souty'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = 0.1

REQUIRED = [
    'lxml',
]

try:
    with open('README.md') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    # The below field needs to be fixed by pypa
    # long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    py_modules=['html2dict'],
    install_requires=REQUIRED,
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
)