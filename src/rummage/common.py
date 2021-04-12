
def truncate(string, size: int = 300, suffix='...'):
    """
    Truncate the given string at a set length with a prefix.

    string: String to truncate
    size: Max size of the string before truncate
    suffix: String that is appended to the truncated string
    """
    return "".join((str(string)[:size - len(suffix)], suffix)) \
        if len(str(string)) > size else str(string)
