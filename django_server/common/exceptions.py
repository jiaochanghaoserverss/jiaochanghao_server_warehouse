class BaseError(Exception):
    status_code = 500   # HTTP STATUS CODE
    _type = "BaseError"

    def __init__(self, message='', code=1, status_code=None):
        self.code = code
        self.message = message
        self.status_code = status_code or self.__class__.status_code

    def __str__(self):
        return "%s: Code:%s status:%s: Msg:%s" % (self._type, self.code, self.status_code, self.message)


class ParamError(BaseError):
    status_code = 400


class Unauthorized(BaseError):
    status_code = 401


class PermissionDenied(BaseError):
    status_code = 403


class ObjectNotFound(BaseError):
    status_code = 404


class ServiceError(BaseError):
    status_code = 500


class ViewError(BaseError):
    status_code = 400


class InternalError(BaseError):
    status_code = 500


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    from rest_framework.views import exception_handler
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data = {'message': str(exc.detail if hasattr(exc, 'detail') else '')}

    return response
