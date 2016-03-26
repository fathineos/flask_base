from functools import wraps
from sys import getsizeof
from flask import g, request, current_app, make_response
from base.lib.exceptions import InterfaceException
from werkzeug.exceptions import UnsupportedMediaType
from base.lib.exceptions import MutableException
from .exceptions import ApiRequestValidationException,\
    ApiRequestMissingParamValidationException, ApiInvalidAccessControlHeader,\
    ApiRequestFileMissingValidationException,\
    ApiRequestFileTooBinValidationException
from . import get_response_from_result, get_parameters_by_method


def validate_request(*validators):
    """Decorator function to wrap the flask api endpoints. Provide validators
    that extend IValidator interface as arguments"""
    def validator_decorator(func):
        @wraps(func)
        def __wrapper(*args, **kwargs):
            try:
                for validator in validators:
                    validator.execute()
            except ApiRequestValidationException, e:
                raise MutableException(e.get_code(), e.get_description())
            return func(*args, **kwargs)
        return __wrapper
    return validator_decorator


class IValidator(object):
    def execute(self):
        raise InterfaceException()


class ParamsValidator(IValidator):
    def __init__(self, required_params):
        self.required_params = required_params

    def execute(self):
        request_params = get_parameters_by_method()
        for param in self.required_params:
            if param not in request_params:
                raise ApiRequestMissingParamValidationException(
                    invalid_param=param)


class FileValidator(IValidator):
    def __init__(self, file_name=None):
        self.file_name = file_name

    def execute(self):
        try:
            return request.files[self.file_name]
        except KeyError:
            raise ApiRequestFileMissingValidationException(
                file_name=self.file_name)


class FileTooBigValidator(IValidator):
    def __init__(self, file_name, size_limit):
        self.file_name = file_name
        self.size_limit = size_limit

    def execute(self):
        FileValidator(file_name=self.file_name)
        f = request.files[self.file_name]
        if getsizeof(f.stream) > self.size_limit:
            raise ApiRequestFileTooBinValidationException(self.size_limit)


def access_cross_origin_resource_sharing_validator(f):
    @wraps(f)
    def add_allow_origin(*args, **kwargs):
        domain = _get_allowed_cross_origin_domain()
        if request.method == "OPTIONS":
            r = make_response()
            r.headers["Access-Control-Allow-Methods"] = \
                "GET, POST, PUT, OPTIONS"
            r.headers["Access-Control-Max-Age"] = 1000
            r.headers["Access-Control-Allow-Headers"] = \
                "origin, x-csrftoken, content-type, accept"
        else:
            r = get_response_from_result(f(*args, **kwargs))
        r.headers["Access-Control-Allow-Origin"] = domain
        return r
    return add_allow_origin


def _get_allowed_cross_origin_domain():
    try:
        domain = request.headers['Origin']
    except KeyError:
        raise ApiInvalidAccessControlHeader()

    if domain in current_app.config['ALLOW_ORIGIN_DOMAINS']:
        g.allow_origin_domain = domain
    else:
        raise ApiInvalidAccessControlHeader()

    return domain


def accepts_mimetypes(supported_types):
    def accepts_mimetypes_decorator(func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            valid = False
            for supported_type in supported_types:
                if supported_type in request.content_type:
                    valid = True
                    break

            if not valid:
                error_str = "Invalid Content-type, accepted types : %s"\
                    % str(supported_type)
                raise UnsupportedMediaType(description=error_str)
            return func(*args, **kwargs)
        return func_wrapper
    return accepts_mimetypes_decorator
