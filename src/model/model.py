# File: model.py
# Purpose: Functions used to evaluate the performance of BERT QA.
from src.process_data.extract.raw2Squad import *
import numpy as np


# Returns the average token length for the answer list.
def avg_token_len(answer_list):
    lengths = []
    for answer in answer_list:
        candidates = answer[1].split()
        lengths += [len(candidates)]
    return np.mean(lengths)


# Evaluates the performance of the BERT QA model.
def bert_accuracy(guess_list, answer_list, h_dict):
    true, count = 0, 0
    short = []
    for key in h_dict.keys():
        short += [key[:10]]
    for i in range(len(guess_list)):
        candidates = answer_list[i][1].split()
        h_count = 0
        for candidate in candidates:
            if candidate in short:
                h_count += 1
        guess = guess_list[i]
        answer = answer_list[i]
        if h_count >= 0:
            count += 1
            if guess == answer[0]:
                true += 1
    return true, count, true / count


# Returns the list of generated predictions.
def get_guesses(guess_file):
    dict_guess = dict_from_json(guess_file)
    guess_list = []
    for key, value in dict_guess.items():
        guess_list += [value]
    return guess_list


# Returns the list of correct answers along with relevant context.
def get_answers(answer_file):
    dict_answer = dict_from_json(answer_file)
    answer_list = []
    for dict_par in dict_answer['data']:
        for context in dict_par['paragraphs']:
            answer_list += [[context['qas'][0]['answers'][0]['text'],
                             context['context'],
                             context['qas'][0]['question']]]
    return answer_list


# Checks if the two lists are correctly generated.
def correct_pair(guess_list, answer_list):
    return len(guess_list) == len(answer_list)
