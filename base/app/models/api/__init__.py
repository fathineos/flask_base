from flask.wrappers import Response
from flask import request, make_response


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
        parameters = request.get_json(silent=True, force=True) or dict()

    return parameters


def get_response_from_result(result):
    if isinstance(result, Response):
        response = result
    else:
        response = make_response(result)
    return response
