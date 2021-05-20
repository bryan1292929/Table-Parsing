# File: unmerge_table.py
# Purpose: Given a table element, returns an unmerged representation as a 2D list containing text.


# Returns an unmerged text matrix for a table.
def unmerge(table):
    text_matrix = []
    # If our table is valid,
    if is_valid(table):
        # Unmerge horizontally.
        text_horizontal, rowspan_horizontal = unmerge_horizontally(table)
        rowspan_matrix = fill_rowspan(rowspan_horizontal)
        # If possible to fully unmerge,
        if len(rowspan_matrix):
            # Unmerge vertically.
            text_matrix = unmerge_vertically(text_horizontal, rowspan_matrix)
    return text_matrix


# Checks if the table is not empty or convoluted.
def is_valid(table):
    # Checks if table contains rows.
    is_non_empty = len(list(table.iter('tr')))
    # Checks if there is no table inside a table.
    is_not_convoluted = no_convolution(table)
    return is_non_empty and is_not_convoluted


# Checks if the table is not convoluted.
def no_convolution(table):
    children = list(table.iter())
    children.pop(0)
    for child in children:
        if child.tag == 'table':
            return False
    return True


# Given a table element, returns the horizontally unmerged text matrix and rowspan matrix.
def unmerge_horizontally(table):
    text_matrix, rowspan_matrix = [], []
    # For each row in the table,
    for row in table.iter('tr'):
        # Get the text list and rowspan list for each row.
        text_list, rowspan_list = extract_row(row)
        # If the row is nonempty,
        if len(text_list):
            # Add each row to the respective matrix.
            text_matrix += [text_list]
            rowspan_matrix += [rowspan_list]
    return text_matrix, rowspan_matrix


# Given a row element, returns the horizontally unmerged text list and rowspan list.
def extract_row(row):
    text_list, rowspan_list = [], []
    # Possible tags of cells that may contain text.
    cell_tags = ['th', 'td', 'te', 'tu']
    # For each cell in the row,
    for cell in row.iter(cell_tags):
        # Extract data from the cell.
        text, rowspan, colspan = extract_cell(cell)
        # Unmerge the row horizontally.
        for i in range(colspan):
            text_list += [text]
            rowspan_list += [rowspan]
    return text_list, rowspan_list


# Extracts text, rowspan and colspan from a table cell.
def extract_cell(cell):
    text, rowspan, colspan = "", 1, 1
    # Concatenate the text.
    for string in cell.itertext():
        text += string
    # Update rowspan and colspan if necessary.
    if 'rowspan' in cell.keys():
        rowspan = max([1, int(cell.get('rowspan'))])
    if 'colspan' in cell.keys():
        colspan = max([1, int(cell.get('colspan'))])
    return text, rowspan, colspan


# Fills the absent values in the horizontally unmerged rowspan matrix.
# The rowspan of each unmerged cell is the number of consecutive cells below (including itself)
# that share the same text.
def fill_rowspan(rowspan_horizontal):
    # For each row,
    for i in range(len(rowspan_horizontal)):
        # First check if the rowspan values of the row are in range.
        if max(rowspan_horizontal[i]) > len(rowspan_horizontal) - i:
            return []
        # For each column index,
        for j in range(len(rowspan_horizontal[0])):
            # Rowspan for current cell.
            rowspan = rowspan_horizontal[i][j]
            # If rowspan is greater than 1,
            if rowspan > 1:
                # Insert (rowspan - 1) in the same column index for the next row.
                rowspan_horizontal[i + 1].insert(j, rowspan - 1)
        # Check if the next row is updated properly.
        in_range = i + 1 < len(rowspan_horizontal)
        not_extended = len(rowspan_horizontal[i]) != len(rowspan_horizontal[i + 1])
        if in_range and not_extended:
            return []
    return rowspan_horizontal


# Vertically unmerges the text matrix according to the fully unmerged rowspan_matrix
def unmerge_vertically(text_horizontal, rowspan_matrix):
    # For each column in the text matrix,
    for j in range(len(text_horizontal[0])):
        # For each cell in the column,
        for i in range(len(text_horizontal) - 1):
            # If the rowspan indicates there are cells below that share the same text,
            if rowspan_matrix[i][j] > 1:
                # Insert text in the appropriate column index in the next row of the text matrix.
                text_horizontal[i + 1].insert(j, text_horizontal[i][j])
    return text_horizontal
