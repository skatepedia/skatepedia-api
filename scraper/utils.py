import re


def parse_integer(str_integer):
    if not str_integer:
        return
    try:
        return int(re.search(r"\d+", str_integer).group())
    except (ValueError, AttributeError):
        pass
