from functools import wraps
from flask import g, request, current_app, make_response
from flask.wrappers import Response
from werkzeug.exceptions import UnsupportedMediaType
from base.app.models.api.exceptions import ApiInvalidAccessControlHeader


def get_parameters_by_method():
    """Get request parameters as a dictionary dynamically depending one the
    request type (GET, POST).
    :type request: flask.request
    :returns dict -- Contains the request parameters as key value pairs
    """

    parameters = dict()
    if request.method == "GET":
        parameters = request.args.copy()
    elif request.method == "POST":
        # works just for json response
        parameters = request.get_json(silent=True) or dict()

    return parameters


# TODO: move to validators class
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


def access_cross_origin_resource_sharing_header(f):
    @wraps(f)
    def add_allow_origin(*args, **kwargs):
        domain = _get_allowed_cross_origin_domain()
        r = _get_response_from_result(f(*args, **kwargs))
        r.headers["Access-Control-Allow-Origin"] = domain
        return r
    return add_allow_origin


def _get_response_from_result(result):
    if isinstance(result, Response):
        response = result
    else:
        response = make_response(result)
    return response


def _get_allowed_cross_origin_domain():
    try:
        domain = request.headers['Origin']
    except KeyError:
        raise ApiInvalidAccessControlHeader()

    if domain in current_app.config['ALLOW_ORIGIN_DOMAINS']:
        g.allow_origin_domain = domain
    else:
        raise ApiInvalidAccessControlHeader

    return domain
