# -*- encoding: utf-8 -*-


class BaseGetResponseError(Exception):
    def __init__(self, message, response, *args, **kwargs):
        self.message = message.encode(encoding='utf-8', errors='strict')
        self.response = response

    def __str__(self):
        return repr(self.message)


class AuthenticationError(BaseGetResponseError):
    pass


class ExternalError(BaseGetResponseError):
    pass


class ForbiddenError(BaseGetResponseError):
    pass


class ManyRequestsError(BaseGetResponseError):
    pass


class NotFoundError(BaseGetResponseError):
    pass


class UniquePropertyError(BaseGetResponseError):
    pass


class ValidationError(BaseGetResponseError):
    pass
