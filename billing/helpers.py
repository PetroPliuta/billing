import re


def is_mac(string=''):
    try:
        return re.search(r"^[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\1[0-9a-f]{2}){4}$", string.lower())
    except:
        return False


def format_mac(string=''):
    try:
        if is_mac(string):
            return re.sub(r'-|:', '', string.lower())
        else:
            return string
    except:
        return string


def is_one_list_in_another_list(one='', two=''):
    """Compares two iterables. Returns True if ANY element of one iterable is in another iterable"""
    try:
        return any(x in one for x in two)
    except:
        return False
