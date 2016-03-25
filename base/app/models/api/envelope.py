from json import dumps
from .exceptions import InvalidEnvelopeException, \
    InvalidEnvelopeParamException, JsonifyEnvelopeException


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
        return self

    def set_error_from_exception(self, e):
        if not (isinstance(e, Exception)):
            raise InvalidEnvelopeParamException
        return self.append_error(e.get_code(), e.get_description())

    def get_errors(self):
        return self._errors

    def set_code(self, code):
        if not (isinstance(code, int)):
            raise InvalidEnvelopeParamException
        self._code = code
        return self

    def get_code(self):
        return self._code

    def set_results(self, results):
        self._results = results
        return self

    def get_results(self):
        return self._results

    def set_message(self, message):
        if not (isinstance(message, str)):
            raise InvalidEnvelopeParamException
        self._message = message
        return self

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

    def to_json(self):
        try:
            result = dumps(self.to_dict())
        except TypeError:
            raise JsonifyEnvelopeException
        return result

    def _is_valid(self):
        if (self.get_results() and self.get_code() and self.get_message())\
                or self.get_errors():
            return True

        return False
