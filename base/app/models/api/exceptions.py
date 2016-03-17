from base.lib.exceptions import ImmutableException


class ApiException(ImmutableException):
    code = 1000
    description = "Generic Api Error"


class InvalidEnvelopeException(ApiException):
    code = 1100
    description = "Invalid Envelope: General Error"


class InvalidEnvelopeParamException(InvalidEnvelopeException):
    code = 1101
    description = "Invalid Envelope: message type Error"


class InvalidEnvelopeResults(InvalidEnvelopeException):
    code = 1102
    description = "Invalid Envelope Results: cannot stringify results"


class JsonifyEnvelopeException(InvalidEnvelopeException):
    code = 1103
    description = "Could not jsonify Envelope"


class ApiValidationInternalException(ApiException):
    code = 2000
    description = "Api Validation Internal Error"


class ApiRequestFileValidationException(ApiException):
    code = 2101
    description = "Api Request Validation Error: File Not Valid"


class ApiInvalidAccessControlHeader(ApiException):
    code = 1001
    description = "Invalid Origin Request Headers"
