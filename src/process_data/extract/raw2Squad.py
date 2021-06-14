# File: raw2Squad.py
# Creates SQuAD-formatted data from raw xml files.
from src.process_data.header_dictionary.header import *
from src.re_util.re_util import *
import json
import random


# Retrieves the dictionary stored in a json file.
def dict_from_json(name):
    with open(name) as json_file:
        dictionary = json.load(json_file)
    return dictionary


# Creates a json file corresponding to the squad formatted data from a folder.
def json_from_folder(folder, name, h_dict):
    data = squad_formatted_data(folder, h_dict)
    with open(name, 'w') as json_file:
        json.dump(data, json_file)


# Creates squad formatted data from a given folder.
def squad_formatted_data(folder, h_dict):
    id_count = 0
    data = []
    for file in files_in_folder(folder):
        paragraphs = []
        for table in tables_in_file(str(file)):
            hdr_idx = header_idx(table)
            if hdr_idx >= 0:
                text_matrix = unmerge(table)
                if len(text_matrix):
                    paragraph, id_count = paragraph_from_table(text_matrix, hdr_idx, id_count, h_dict)
                    paragraphs += paragraph
        if len(paragraphs):
            data += [{'paragraphs': paragraphs, 'title': str(file)}]
    return {'version': 'v2.0', 'data': data}


# Returns a paragraph dictionary from a table.
def paragraph_from_table(text_matrix, hdr_idx, id_count, h_dict):
    paragraph = []
    windows = candidate_windows(clean_matrix(text_matrix), hdr_idx, h_dict)
    random.shuffle(windows)
    for window in windows:
        question, text, candidates, h_count, has_answer = window
        # Concatenate the text for each candidate.
        context = ""
        for candidate in candidates:
            context += candidate + " "
        context = context[:-1]
        # Q&A.
        if has_answer:
            answer_list = [{'answer_start': context.index(text), 'text': text}]
        else:
            answer_list = []
        qas = {
            'answers': answer_list,
            'is_impossible': not has_answer,
            'question': question,
            'id': 'id:' + str(id_count),
            'h_count': h_count
        }
        id_count += 1
        dict_window = {'context': context, 'qas': [qas]}
        paragraph += [dict_window]
    return paragraph, id_count


# Returns candidate windows for each cell in a text matrix.
def candidate_windows(text_matrix, hdr_idx, h_dict):
    # 2D list of candidate windows for each data cell.
    windows = []
    # For each cell in the table,
    for i in range(len(text_matrix)):
        for j in range(len(text_matrix[0])):
            vertical, horizontal = [], []
            # Append prior cells in the same column.
            h_count = 0
            for a in index_list(i, 5, 2):
                if text_matrix[a][j] in h_dict.keys():
                    h_count += 1
                vertical += [whole(text_matrix[a][j][:10])]
            # Append prior cells in the same row.
            for b in index_list(j, 5, 2):
                if text_matrix[i][b] in h_dict.keys():
                    h_count += 1
                horizontal += [whole(text_matrix[i][b][:10])]
            # Current cell (question).
            cell = whole(text_matrix[i][j][:10])
            # Current header (answer).
            header = whole(text_matrix[hdr_idx][j][:10])
            has_answer = header in horizontal + vertical
            if len(horizontal + vertical):
                answer_in_dict = text_matrix[hdr_idx][j] in h_dict.keys()
                if has_answer and answer_in_dict and random.randint(1, 8) == 1:
                    # Append the completed window to the list of windows.
                    if random.choice([True, False]):
                        windows += [[cell, header, horizontal + vertical, h_count, has_answer]]
                    else:
                        windows += [[cell, header, vertical + horizontal, h_count, has_answer]]
    return windows


# Selects the first m and last n tokens.
def index_list(curr, first, last):
    idx_first = list(range(min(curr, first)))
    idx_last = list(range(max(curr - last, 0), curr))
    return list(set(idx_first + idx_last))


# Replaces empty strings with the character '*'
def whole(input_str):
    return input_str if len(input_str) else "*"
