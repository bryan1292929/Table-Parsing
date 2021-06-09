# File: baseline_json.py
# Purpose: Rule-based baseline performance on a json test file.
import random


# Returns the baseline performance for a json test file.
def baseline_accuracy(dict_test, h_dict):
    true, count = 0, 0
    # For paragraphs,
    for dict_par in dict_test['data']:
        # For each candidate window,
        for contexts in dict_par['paragraphs']:
            if contexts['qas'][0]['is_impossible']:
                answer = ""
            else:
                answer = contexts['qas'][0]['answers'][0]['text']
            context = contexts['context']
            candidates = [y for y in context.split()]
            random.shuffle(candidates)
            counts = []
            h_count = 0
            for candidate in candidates:
                if candidate in h_dict.keys():
                    h_count += 1
                    counts += [h_dict[candidate]]
                else:
                    counts += [0]
            guess = candidates[counts.index(max(counts))]
            if max(counts):
                count += 1
                if answer == guess:
                    true += 1
    return true, count, true/count
