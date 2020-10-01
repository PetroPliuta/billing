import re


def is_mac(string):
    return re.search(r"^[0-9a-f]{2}([-:]?[0-9a-f]{2}){5}$", string.lower())


def format_mac(string):
    return re.sub(r'-|:', '', string.lower())
