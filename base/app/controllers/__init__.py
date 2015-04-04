from functools import wraps
from flask import jsonify, request
from werkzeug.exceptions import UnsupportedMediaType


# def json_response(f):
#     """Function decorator that transforms flask route method output to its
#     corresponding json representation.
#     :returns str -- json representation of the function's return value
#     """
#     @wraps(f)
#     def json_response_decorator(*args, **kwargs):
#         return jsonify(f(*args, **kwargs))
#     return json_response_decorator


def get_parameters_by_method(request):
    """Get request parameters as a dictionary dynamically depending one the
    request type (GET, POST).
    :param request: Flask HTTP request object dispatched
    :type request: flask.request
    :returns dict -- Contains the request parameters as key value pairs
    """
    # try:
    #     request.url_root
    #     global url_root
    #     url_root = request.url_root
    # except AttributeError:
    #     pass

    parameters = dict(method=None)
    request_parameters = dict()

    if request.method == "GET":
        request_parameters = request.args.copy()
    elif request.method == "POST":
        #works just for json response
        request_parameters = request.get_json(silent=True) or dict()
    parameters.update(request_parameters.iteritems())

    return parameters


def accepts_mimetypes(supported_types):
    def accepts_mimetypes_decorator(func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            if request.content_type not in supported_types:
                error_str = "Content-type must be set to one of the types : %s"\
                            % str(supported_types)
                raise UnsupportedMediaType(description=error_str)
            return func(*args, **kwargs)
        return func_wrapper
    return accepts_mimetypes_decorator


def set_http_code(success_code):
    def set_http_code_decorator(func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if isinstance(result, tuple):
                return result
            else:
                return result, success_code
        return func_wrapper
    return set_http_code_decorator


def jsonify_reponse_object(f):
    @wraps(f)
    def jsonify_response_decorator(*args, **kwargs):
        result = f(*args, **kwargs)
        if isinstance(result, tuple):
            response, status_code = result
        else:
            response = result
            status_code = None
        try:
            return jsonify(response.to_dict()), status_code
        except AttributeError:
            raise AttributeError(
                "Method to_dict() cannot be found for result object.")
    return jsonify_response_decorator
