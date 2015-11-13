from json import dumps
from flask import current_app, Response, g
from base.app.models.api.envelope import Envelope
from base.app.models.api import exceptions as base_exceptions
from base.app.models.api.exceptions import ApiException, \
    InvalidEnvelopeException, ApiValidationInternalException, \
    ApiRequestFileValidationException, ApiInvalidAccessControlHeader, \
    InvalidEnvelopeParamException, InvalidEnvelopeResults

ERROR_TO_HTTP_CODE_MAPPING = {ApiException.code: 500,
                              InvalidEnvelopeException.code: 500,
                              InvalidEnvelopeParamException.code: 500,
                              InvalidEnvelopeResults.code: 500,
                              ApiValidationInternalException.code: 500,
                              ApiRequestFileValidationException.code: 500,
                              ApiInvalidAccessControlHeader.code: 500}


def error_handler(error):
    """Error handle for all exceptions thrown by the application it is
    registered on. Creates response by converting the error to the relevant
    json response structure that Base uses.

    :param error: Any subclass object of Exception class
    :return: flask.Response
    """

    msg = "Request resulted in {}".format(error)

    if current_app.testing is not True:
        current_app.logger.error(msg, exc_info=error)

    check_and_set_default_error_code_and_description(error)
    envelope = Envelope().set_error_from_exception(error)

    http_code = 500
    if isinstance(error, base_exceptions.ApiException):
        try:
            http_code = ERROR_TO_HTTP_CODE_MAPPING[error.code]
        except KeyError:
            http_code = 500

    try:
        domain = g.allow_origin_domain
        headers = {'Access-Control-Allow-Origin': domain}
    except AttributeError:
        headers = None

    return Response(dumps(envelope.to_dict()),
                    status=int(http_code),
                    mimetype='application/json', headers=headers)


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
