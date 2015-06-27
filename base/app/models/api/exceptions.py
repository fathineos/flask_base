class ApiException(Exception):
    code = 1000
    http_code = 500
    description = "Generic Api Error"

    def __init__(self):
        Exception.__init__(self, self.code, self.description)


class InvalidEnvelopeException(ApiException):
    code = 1100
    description = "Invalid Envelope: General Error"


class InvalidEnvelopeParamException(ApiException):
    code = 1101
    description = "Invalid Envelope: message type Error"


class InvalidEnvelopeResults(ApiException):
    code = 1102
    description = "Invalid Envelope Results: cannot stringify results"


class ApiValidationException(ApiException):
    code = 2000
    http_code = 400
    description = "Api Validation Error"
