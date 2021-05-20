# File: main.py
from model.model import *
from model.baseline import *


if __name__ == '__main__':
    main_dir = 'C:/Users/bryan314/PycharmProjects/TableParsing'
    # folder = main_dir + '/data/raw/202003_train'
    # h_dict = pickle_from_folder(folder, True, main_dir + '/data/dictionary/h_dict_fin.pickle')
    h_dict = dict_from_pickle(main_dir + '/data/dictionary/h_dict_fin.pickle')
    # json_from_folder(main_dir + '/data/raw/202003_train',
    #                  main_dir + '/data/apply/train_str10_num_5_2_full.json', h_dict)
    # json_from_folder(main_dir + '/data/raw/202003_test',
    #                  main_dir + '/data/apply/test_str10_num_5_2_with_head_with_h.json', h_dict)

    # answer_file = main_dir + '/data/apply/sample_horizontal.json'
    # answer_list = get_answers(answer_file)
    # print(len(answer_list))
    # print(json.dumps(dict_from_json(answer_file), indent=4, ensure_ascii=False))
    # print(avg_token_len(answer_list))

    guess_file = main_dir + '/output/modelC/sample/sample_horizontal/predictions.json'
    guess_list = get_guesses(guess_file)
    answer_file = main_dir + '/data/apply/sample_horizontal.json'
    answer_list = get_answers(answer_file)
    print(len(answer_list))
    print(avg_token_len(answer_list))
    print(bert_accuracy(guess_list, answer_list, h_dict))
    print(baseline_accuracy(dict_from_json(answer_file), h_dict))

