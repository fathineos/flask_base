from flask import current_app, Response, g
from .app.models.api.envelope import Envelope
from werkzeug.exceptions import BadRequest, InternalServerError
from .lib.exceptions import IException, MutableException
from .app.models.api.exceptions import InvalidEnvelopeException,\
    ApiInvalidAccessControlHeader, ApiRequestValidationException, ApiException


"""Exceptions to HTTP code mapping in order to avoid generic 500 error and give
more specific error codes.
In python it is not possible to check if an object is exact instance of a class
or a subclass. In the way that the mapping is implemeted, the inheritance of
exception matters.
"""
ERROR_TO_HTTP_CODE_MAPPING = {
    InvalidEnvelopeException: InternalServerError.code,
    ApiInvalidAccessControlHeader: BadRequest.code,
    ApiRequestValidationException: BadRequest.code}


def exception_handler(exc):
    """Error handle for all exceptions thrown by the application it is
    registered on. Creates response by converting the error to the relevant
    json response structure that Base uses.

    :param error: Any subclass object of Exception class
    :return: flask.Response
    """

    msg = "Request resulted in {}".format(exc)

    if current_app.testing is not True:
        current_app.logger.error(msg, exc_info=exc)

    http_code = InternalServerError.code
    if isinstance(exc, IException):
        for exc_class, code in ERROR_TO_HTTP_CODE_MAPPING.iteritems():
            if isinstance(exc, exc_class):
                http_code = code
                break
    else:
        exc = MutableException(ApiException().get_code(), exc.message)

    envelope = Envelope().set_error_from_exception(exc)

    headers = _set_allow_origin_domain_header()

    return Response(envelope.to_json(),
                    status=int(http_code),
                    mimetype='application/json',
                    headers=headers)


def _set_allow_origin_domain_header():
    """Set allow origin domain headers if the request had valid Origin in
    headers. The allow_origin_domain is set from
    access_cross_origin_resource_sharing_validator in package
    base.app.models.api.validators"""
    try:
        domain = g.allow_origin_domain
        headers = {'Access-Control-Allow-Origin': domain}
    except AttributeError:
        headers = None
    return headers
