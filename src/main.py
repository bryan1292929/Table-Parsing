# File: main.py
from model.model import *
from model.baseline import *
import random

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main_dir = 'C:/Users/bryan314/PycharmProjects/TableParsing'
    # folder = main_dir + '/data/raw/202003_train'
    # h_dict = pickle_from_folder(folder, True, main_dir + '/data/dictionary/new_h_dict.pickle')
    h_dict = dict_from_pickle(main_dir + '/data/dictionary/h_dict_fin.pickle')

    tables = []
    count = 0
    main_dir = 'C:/Users/bryan314/PycharmProjects/TableParsing'
    for file in files_in_folder(main_dir + '/data/raw/202003_test'):
        for table in tables_in_file(str(file)):
            if header_idx(table) >= 0 and len(unmerge(table)) - header_idx(table) > 2:
                if rowspan_guess(table) > 2 and rowspan_guess(table) == colspan_guess(table):
                    count += 1
                    print(count)
                    hor_idx = header_idx(table)
                    ver_idx = rowspan_guess(table) - 1
                    print(header_idx(table), ver_idx)
                    matrix = clean_matrix(unmerge(table))
                    original = unmerge(table)
                    for line in original:
                        print(line)
                    print('-----------------')
                    for i in range(hor_idx + 1, len(matrix)):
                        for j in range(ver_idx + 1, len(matrix[0])):
                            body = remove_white(original[i][j])
                            hdr_up = ""
                            hdr_left = ""
                            for a in range(hor_idx + 1):
                                if matrix[a][j] != '단위' and original[a][j] != "":
                                    if a == 0 or (a > 0 and matrix[a][j] != matrix[a - 1][j]):
                                        hdr_up += remove_white(original[a][j]) + ";"
                            for b in range(ver_idx + 1):
                                if original[i][b] != "":
                                    if b == 0 or b > 0 and matrix[i][b] != matrix[i][b - 1]:
                                        hdr_left += remove_white(original[i][b]) + ";"
                            hdr_up = hdr_up[:-1]
                            hdr_left = hdr_left[:-1]
                            if remove_special(remove_white(body)) != "":
                                cond = True
                                for b in range(ver_idx + 1):
                                    if remove_white(original[i][b]) == body:
                                        cond = False
                                if cond:
                                    print(hdr_left, '&', hdr_up, ':', body)
                    print('---------------------')
