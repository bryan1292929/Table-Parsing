# File: unify_dates.py
# Purpose: Unifies various representations of dates in a text.
import re

# Dictionary from month to number of maximum days in a month.
month_to_day = {1: 31, 2: 29, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}


# Function that cleans dates in a given string.
def clean_dates(input_str):
    input_str = char_for_year(input_str)
    input_str = word_for_year(input_str)
    input_str = unify_dates(input_str)
    return input_str


# --------------------------Simple Functions--------------------------
# Translates years written symbolically to their numeric forms.
def char_for_year(input_str):
    p = re.compile('[\'`‘’](?=[0-9]{2})')
    return p.sub('20', input_str)


# Adds the word representing years to keys of the form 20XX.
def word_for_year(input_str):
    p = re.compile('('
                   '(?<=\A)20[0-9]{2}(?=\Z)'  # When the year is by itself numerically.
                   '|'
                   '(?<![0-9~-])20[0-9]{2}[~-]20[0-9]{2}(?![0-9~-])'  # For year-to-year ranges.
                   ')'
                   , re.VERBOSE)
    return p.sub(helper_for_word, input_str)


# Helper function for word_for_year.
def helper_for_word(input_match):
    p = re.compile('(20[0-9]{2})')
    return p.sub('\g<0>년', input_match.group())


# --------------------------Higher Functions--------------------------
# Reduces dates in a string to a single format, 년/월/일 or 년/월.
def unify_dates(input_str):
    # Find dates that include the year, month and optionally the day.
    p = re.compile('(?<![0-9])'  # Condition for beginning of the date.
                   '([0-9]{2}|[0-9]{4})[년./-]'  # Guranteed numeric year and symbol.
                   '[0-9]{1,2}'  # Guranteed numeric month.
                   '('
                   '[월./-][0-9]{1,2}일?'  # Case 1: Month and day
                   '|'
                   '월?'  # Case 2: Only month
                   ')'
                   '(?![0-9%])',  # Condition for end of the date.
                   re.VERBOSE)
    # Clean each type of date.
    input_str = p.sub(change_date, input_str)

    return input_str


# Changes a full date to the given format.
def change_date(input_match):
    date = input_match.group()
    # Change the year.
    date, year = change_year(date)
    # Change the month.
    date, month = change_month(date)
    # If the month is invalid, return the original string.
    if month < 1 or month > 12:
        return input_match.group()
    # Change the day.
    date, day = change_day(date, month)
    # If the day is invalid, return the original string.
    if day < 1 or day > month_to_day[month]:
        return input_match.group()
    # Consider leap years.
    if month == 2 and day == 29 and not is_leap(year):
        return input_match.group()
    # Return the proper date.
    return date


# Given a year, determines if it is a leap year.
def is_leap(year):
    if year % 4 == 0 and year % 100 != 0:
        return True
    if year % 4 == 0 and year % 100 == 0 and year % 400 == 0:
        return True
    return False


# Given a string of the date, changes the format of the year.
def change_year(date):
    # We begin with the year.
    p_year = re.compile('([0-9]{2,4})년?')
    year = p_year.search(date).group(1)
    if int(year) < 100:
        year = '20' + year
    date = p_year.sub(year + '년', date, count=1)
    return date, int(year)


# Given a string of the date, changes the format of the month.
def change_month(date):
    # We now move on to the month.
    p_month = re.compile('(?<=년)[./-]?([0-9]{1,2})월?')
    month = int(p_month.search(date).group(1))
    if 1 <= month <= 12:
        date = p_month.sub(str(month) + '월', date, count=1)
    return date, month


# Given a string of the date, changes the day of the month.
def change_day(date, month):
    p_day = re.compile('(?<=월)[./-]?([0-9]{1,2})일?')
    day_search = p_day.search(date)
    if day_search:
        day = int(day_search.group(1))
    # When there is no date at all and the date format is 년/월.
    else:
        return date, 1
    if 1 <= day <= month_to_day[month]:
        date = p_day.sub(str(day) + '일', date, count=1)
    return date, day
