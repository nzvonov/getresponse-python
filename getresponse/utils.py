# -*- encoding: utf-8 -*-
from __future__ import unicode_literals


def snake_to_camel(snake_string):
    """
    Format string from snake_case to camelCase.
    :param snake_string: string in snake_case format
    :return: string in camelCase format
    """
    splitter = '_'
    split_field = snake_string.split(splitter)
    titled_words = [word.title() for word in split_field[1:]]
    camel_string = ''.join(split_field[:1] + titled_words)
    return camel_string
