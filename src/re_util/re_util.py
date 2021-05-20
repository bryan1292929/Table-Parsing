# File: re_util.py
# Purpose: Provides regular expressions to process text.
import re
from src.re_util.unify_dates import clean_dates
from src.re_util.unify_synonyms import clean_synonyms


# Returns a new matrix with clean text for each cell.
def clean_matrix(text_matrix):
    new_matrix = []
    for i in range(len(text_matrix)):
        new_row = []
        for j in range(len(text_matrix[0])):
            new_row += [clean(text_matrix[i][j])]
        new_matrix += [new_row]
    return new_matrix


# Cleans a string that acts as a key or value.
def clean(input_str):
    input_str = remove_white(input_str)
    input_str = clean_dates(input_str)
    input_str = clean_synonyms(input_str)
    input_str = remove_parentheses(input_str)
    input_str = remove_colons(input_str)
    input_str = remove_special(input_str)
    return input_str


# Functions to use to clean the text (key and values).
def remove_white(input_str):
    p = re.compile('(\s|&cr;|\xad)')
    return p.sub('', input_str)


# Clean up parentheses in keys.
def remove_parentheses(input_str):
    p1 = re.compile('\A[(](.*)[)]\Z')
    key = p1.search(input_str)
    if key:
        input_str = p1.sub(key.group(1), input_str)
    p2 = re.compile('[(].*[)]')
    input_str = p2.sub('', input_str)
    return input_str


# Clean up colons in keys.
def remove_colons(input_str):
    p = re.compile(':.*')
    return p.sub('', input_str)


# Clean up special characters in keys.
def remove_special(input_str):
    p = re.compile('[^가-힣0-9]')
    return p.sub('', input_str)
