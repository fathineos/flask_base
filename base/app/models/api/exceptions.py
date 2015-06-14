class ApiException(Exception):
    code = 1000
    description = "Generic Api Error"

    def __init__(self):
        Exception.__init__(self, self.code, self.description)


class InvalidEnvelopeException(ApiException):
    code = 1100
    description = "Invalid Envelope: General Error"


class InvalidEnvelopeParamException(ApiException):
    code = 1101
    description = "Invalid Envelope: message type Error"
