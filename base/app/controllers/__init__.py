from functools import wraps
from flask import g, jsonify, request, current_app
from werkzeug.exceptions import UnsupportedMediaType
from base.app.models.api.exceptions import ApiInvalidAccessControlHeader


def json_response(f):
    """Function decorator that transforms flask route method output to its
    corresponding json representation.
    :returns str -- json representation of the function's return value
    """
    @wraps(f)
    def json_response_decorator(*args, **kwargs):
        return jsonify(f(*args, **kwargs))
    return json_response_decorator


def get_parameters_by_method(request):
    """Get request parameters as a dictionary dynamically depending one the
    request type (GET, POST).
    :param request: Flask HTTP request object dispatched
    :type request: flask.request
    :returns dict -- Contains the request parameters as key value pairs
    """

    parameters = dict()
    if request.method == "GET":
        parameters = request.args.copy()
    elif request.method == "POST":
        #works just for json response
        parameters = request.get_json(silent=True) or dict()

    return parameters


#move to validators class
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
                error_str = "Content-type must be set to one of the types : %s"\
                    % str(supported_type)
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


def access_control_header(f):
    @wraps(f)
    def add_allow_origin(*args, **kwargs):
        allow_origin_header = _get_allow_origin_header(request)
        result = f(*args, **kwargs)

        response = result
        code = None
        headers = None
        if isinstance(result, tuple):
            response, code, headers = result

        if headers:
            headers.update(allow_origin_header)
        else:
            headers = allow_origin_header
        return response, code, headers
    return add_allow_origin


def _get_allow_origin_header(request):
    try:
        domain = request.headers['Origin']
    except AttributeError, KeyError:
        raise ApiInvalidAccessControlHeader()

    if domain in current_app.config['ALLOW_ORIGIN_DOMAINS']:
        g.allow_origin_domain = domain
    else:
        raise ApiInvalidAccessControlHeader()

    return {'Access-Control-Allow-Origin': domain}
