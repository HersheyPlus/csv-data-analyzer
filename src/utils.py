def split_and_join(list_of_strings: list, separator: str = ' | ') -> str:
    return separator.join(' '.join(s.split()) for s in list_of_strings)
