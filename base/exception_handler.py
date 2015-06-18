from werkzeug import exceptions
from flask import current_app, Response, json
from base.app.models.api.envelope import Envelope
from base.app.models.api import exceptions as base_exceptions


def error_handler(error):
    """Error handle for all exceptions thrown by the application it is registered on.
    Creates response by converting the error to the relevant json response structure
    that Base uses.

    :param error: Any subclass object of Exception class
    :return: flask.Response
    """

    msg = "Request resulted in {}".format(error)

    if current_app.testing is not True:
        current_app.logger.error(msg, exc_info=error)

    check_and_set_default_error_code_and_description(error)
    envelope = Envelope().set_error_from_exception(error)

    if isinstance(error, base_exceptions.ApiException):
        error.code = error.http_code

    return Response(json.dumps(envelope.to_dict()), status=error.code)


def check_and_set_default_error_code_and_description(error):
    """Checks if the error contains a code and description and sets the default
    values to these properties when they are not available.

    :param error: Any subclass object of Exception class
    """
    description = "Fatal Error"
    code = 500

    try:
        error.description
    except AttributeError:
        error.description = description

    try:
        error.code
    except AttributeError:
        error.code = code
