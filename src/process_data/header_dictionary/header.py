# File: header.py
# Purpose: Functions for the header index of a table element.
# The header index is the row index of the final row in the header.
import csv
import pickle
from src.process_data.extract.traverse_data import *
from src.process_data.extract.unmerge_table import *
from src.re_util.re_util import *


# Returns the vertical-slice guess by the rowspan rule.
def rowspan_guess(table):
    row_list = [0]
    if is_valid(table):
        # Unmerge horizontally.
        _, rowspan_horizontal = unmerge_horizontally(table)
        rowspan_matrix = fill_rowspan(rowspan_horizontal)
        for i in range(header_idx(table) + 1, len(rowspan_matrix)):
            count = 1
            line = rowspan_matrix[i]
            for j in range(len(line) - 1):
                # If the rowspan decreases,
                if line[j] > line[j + 1]:
                    count += 1
                # Neglect cases where the rowspan increases.
                elif line[j] < line[j + 1]:
                    return 0
            # Length of max sequence (of decreasing rowspan) for the current row.
            row_list += [count]
    return max(row_list)


# Returns the vertical-slice guess by the colspan rule.
def colspan_guess(table):
    col_list = [0]
    if header_idx(table) >= 0:
        n_col = len(unmerge(table)[0])
        row_list = list(table.iter('tr'))
        i = 0
        while i < len(row_list):
            cell = list(row_list[i].iter(['th', 'td', 'te', 'tu']))[0]
            rowspan, colspan = 1, 1
            if 'rowspan' in cell.keys():
                rowspan = max([1, int(cell.get('rowspan'))])
            if 'colspan' in cell.keys():
                colspan = max([1, int(cell.get('colspan'))])
            # Neglect cases where the entire row is a single cell.
            if colspan != n_col:
                col_list += [colspan]
            # Jump to the cell below (which is in the first column).
            i += rowspan
    return max(col_list)


# Returns the header index for a given table.
def header_idx(table):
    hdr_idx = -1
    if is_valid(table):
        for thead in table.iter('thead'):
            hdr_idx = len(list(thead.iter('tr'))) - 1
    return hdr_idx


# Combines two dictionaries.
def combine_dict(dict_prev, dict_new):
    for key in dict_new.keys():
        if key in dict_prev.keys():
            dict_prev[key] += dict_new[key]
        else:
            dict_prev[key] = dict_new[key]
    return dict_prev


# Creates a csv file from a header dictionary.
def csv_from_dict(h_dict, name):
    with open(name, 'w') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in h_dict.items():
            writer.writerow([key, value])


# Retrieve processed dictionary from pickle.
def dict_from_pickle(name):
    with open(name, 'rb') as handle:
        h_dict_raw = pickle.load(handle)
    # Select top 1000 keys from h_dict_raw.
    h_dict_sorted = {k: v for k, v in sorted(h_dict_raw.items(), key=lambda item: item[1], reverse=True)}
    h_dict_fin = {k: h_dict_sorted[k] for k in list(h_dict_sorted)[:1000]}
    del h_dict_fin['']
    return h_dict_fin


# Create a pickle file for the header dictionary created from a folder.
def pickle_from_folder(folder, index_type, name):
    data = h_dict_for_folder(folder, index_type)
    with open(name, 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)


# Given a folder of xml files, returns a dictionary that maps from (header cell text) -> count.
def h_dict_for_folder(folder, index_type):
    # Initialize dictionary to return.
    h_dict_folder = {}
    # For each xml file,
    for file in files_in_folder(folder):
        file_name = str(file)
        h_dict_file = h_dict_for_file(file_name, index_type)
        h_dict_folder = combine_dict(h_dict_folder, h_dict_file)
    return h_dict_folder


# Given a xml file, returns a dictionary that maps from (header cell text) -> count.
def h_dict_for_file(file, index_type):
    # Initialize list of matrices and indices to return.
    h_dict_file = {}
    for table in tables_in_file(file):
        h_dict_table = h_dict_for_table(table, index_type)
        h_dict_file = combine_dict(h_dict_file, h_dict_table)
    return h_dict_file


# Given a table, returns a dictionary that maps from (header cell text) -> count.
# index_type: True, cells in final row of header. False, all cells in the header.
def h_dict_for_table(table, index_type):
    h_dict_table = {}
    hdr_idx = header_idx(table)
    if hdr_idx >= 0:
        text_matrix = unmerge(table)
        if len(text_matrix):
            idx_begin = hdr_idx if index_type else 0
            for i in range(idx_begin, hdr_idx + 1):
                for j in range(len(text_matrix[0])):
                    key = clean(text_matrix[i][j])
                    if key in h_dict_table.keys():
                        h_dict_table[key] += 1
                    else:
                        h_dict_table[key] = 1
    return h_dict_table
