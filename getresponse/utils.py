# -*- encoding: utf-8 -*-


def snake_to_camel(snake_string):
    """
    Format string from snake_case to camelCase.

    Args:
        snake_string: string in snake_case format.

    Returns:
        return: string in camelCase format
    """
    splitter = '_'
    split_field = snake_string.split(splitter)
    titled_words = [word.title() for word in split_field[1:]]
    return ''.join(split_field[:1] + titled_words)
