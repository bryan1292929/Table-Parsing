# File: unify_synonyms.py
# Purpose: Unifies synonyms.
import re


# Groups together words with similar meaning which are related to dates.
def clean_synonyms(input_str):
    input_str = unify_periods(input_str)
    input_str = replace_words(input_str, '이상', '초과')
    input_str = replace_words(input_str, '상승', '증가')
    input_str = replace_words(input_str, '이하', '미만')
    input_str = replace_words(input_str, '이내', '미만')
    input_str = replace_words(input_str, '하락', '감소')
    input_str = replace_words(input_str, '수준1', '수준')
    input_str = replace_words(input_str, '수준2', '수준')
    input_str = replace_words(input_str, '수준3', '수준')
    return input_str


# Unifies periods representing years.
def unify_periods(input_str):
    p = re.compile('제?[0-9]+([(]당[)])?([(]전[)])?((?=기)|(?=호))')
    return p.sub('제n', input_str)


# Replaces words in a given string.
def replace_words(input_str, old_str, new_str):
    p = re.compile(old_str)
    return p.sub(new_str, input_str)
