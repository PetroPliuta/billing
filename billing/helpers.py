def is_mac(string):
    import re
    return re.match("^[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", string.lower())


def format_mac(string):
    return string.lower().replace('-', '').replace(':', '')
