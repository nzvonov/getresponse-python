# -*- encoding: utf-8 -*-
from __future__ import unicode_literals


class BaseGetResponseError(Exception):
    def __init__(self, message, response, *args, **kwargs):
        super(BaseGetResponseError).__init__(message, *args, **kwargs)
        self.response = response


class UniquePropertyError(BaseGetResponseError):
    pass


class NotFoundError(BaseGetResponseError):
    pass


class ValidationError(BaseGetResponseError):
    pass


class ForbiddenError(BaseGetResponseError):
    pass
