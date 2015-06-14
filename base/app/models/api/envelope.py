from .exceptions import InvalidEnvelopeException, InvalidEnvelopeParamException


class Envelope(object):
    def __init__(self):
        self._errors = []
        self._code = None
        self._results = None
        self._message = None

    def append_error(self, code, message):
        error = {
            "code": code,
            "message": message,
        }
        self._errors.append(error)

    def set_error_from_exception(self, e):
        if not (isinstance(e, Exception)):
            raise InvalidEnvelopeParamException
        return self.set_error(e.code, e.description)

    def get_errors(self):
        return self._errors

    def set_code(self, code):
        if not (isinstance(code, int)):
            raise InvalidEnvelopeParamException
        self._code = code

    def get_code(self):
        return self._code

    def set_results(self, results):
        self._results = results

    def get_results(self):
        return self._results

    def set_message(self, message):
        if not (isinstance(message, str)):
            raise InvalidEnvelopeParamException
        self._message = message

    def get_message(self):
        return self._message

    def to_dict(self):
        if self._is_valid() is False:
            raise InvalidEnvelopeException()

        return {
            "results": self.get_results(),
            "message": self.get_message(),
            "code": str(self.get_code()),
            "errors": self.get_errors()
        }

    def _is_valid(self):
        if (self.get_results() and self.get_code() and self.get_message())\
                or self.get_errors():
            return True

        return False