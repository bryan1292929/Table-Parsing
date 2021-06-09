# File: traverse_data.py
# Purpose: Provides functions to traverse tables in xml files and folders.
from pathlib import Path
from lxml import etree


# Returns a collection of xml files in a folder.
def files_in_folder(folder):
    return Path(folder).rglob('*.xml')


# Returns an iterator through tables in an xml file.
def tables_in_file(file):
    parser = etree.HTMLParser()
    tree = etree.parse(file, parser)
    root = tree.getroot()
    return root.iter('table')


# Returns the file type of the given file.
def file_type(file):
    parser = etree.HTMLParser()
    tree = etree.parse(file, parser)
    root = tree.getroot()
    name = list(root.iter('document-name'))
    if len(name):
        return name[0].text
    return ""
