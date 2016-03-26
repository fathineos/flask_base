from base.lib.exceptions import ImmutableException


class ApiException(ImmutableException):
    _code = 1000
    _description = "Generic Api Error"


class InvalidEnvelopeException(ApiException):
    _code = 1100
    _description = "Invalid Envelope: General Error"


class InvalidEnvelopeParamException(InvalidEnvelopeException):
    _code = 1101
    _description = "Invalid Envelope: message type Error"


class InvalidEnvelopeResults(InvalidEnvelopeException):
    _code = 1102
    _description = "Invalid Envelope Results: cannot stringify results"


class JsonifyEnvelopeException(InvalidEnvelopeException):
    _code = 1103
    _description = "Could not jsonify Envelope"


class ApiRequestValidationException(ImmutableException):
    """The request validator exceptions should extend this class"""
    _code = 1200
    _description = "Request Validation Error"


class ApiRequestMissingParamValidationException(ApiRequestValidationException):
    _code = 1201
    _description = "Request parameters not valid"

    def __init__(self, invalid_param=None):
        if invalid_param:
            self._description = "Missing request parameter '{}'".format(
                invalid_param)
        message = "Exception {}: {}".format(self._code, self._description)
        Exception.__init__(self, message)


class ApiRequestFileMissingValidationException(ApiRequestValidationException):
    _code = 1202
    _description = "File Not Valid"

    def __init__(self, file_name=None):
        if file_name:
            self._description = "File {} Missing".format(file_name)
        message = "Exception {}: {}".format(self._code, self._description)
        Exception.__init__(self, message)


class ApiRequestFileTooBinValidationException(ApiRequestValidationException):
    _code = 1202
    _description = "File too big"

    def __init__(self, size_limit=None):
        if size_limit:
            self._description = "File larger than {} bytes".format(size_limit)
        message = "Exception {}: {}".format(self._code, self._description)
        Exception.__init__(self, message)


class ApiInvalidAccessControlHeader(ApiRequestValidationException):
    _code = 1203
    _description = "Invalid Origin Request Headers"
