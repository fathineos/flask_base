"""Exception classes to extend BasicException functionality. The basic
types provided are MutableException and ImmutableException. Both shall
have the same interface."""


class MutableException(Exception):
    """
    This exception class extends python's basic exception and allows you to set
    custom code and description
    :param code: an exception code
    :param message: a description of the exception
    :type code: int
    :type message: str
    """
    def __init__(self, code, description):
        self.code = code
        self.description = description
        message = "Exception {}: {}".format(self.code, self.description)
        Exception.__init__(self, message)


class ImmutableException(Exception):
    """
    This exception class extends python's basic exception. The code, and
    description is immutable. Extend this class to create more specific
    exceptions.
    """
    code = 1000
    description = "Generic Error"

    def __init__(self):
        message = "Exception {}: {}".format(self.code, self.description)
        Exception.__init__(self, message)


class LibraryException(ImmutableException):
    code = 3000
    description = "Generic Library Error"


class NoTimezoneSet(LibraryException):
    code = 3001
    description = "No timezone set"
